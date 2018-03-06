#!/usr/bin/python

# Implementing your own inverted indexer.

import cPickle as pickle
import errno
import os
import re
from collections import Counter, defaultdict

from bs4 import BeautifulSoup

__inverted_index__ = defaultdict(dict)
__token_index__ = {}
__term_frequency__ = {}
__corpus_statistics__ = {'CORPUS_LENGTH': 0, 'TOTAL_DOCUMENTS': 0}
__token_directory__ = 'corpus'
__n_gram__ = 1


# args: BASE_DIRECTORY, RAW_HTML_DIRECTORY, TOKEN_DIRECTORY, STOPLIST, N_GRAM
def __generate_inverted_index__(args):
    __make_corpus__({
        'RAW_HTML_DIRECTORY': args['RAW_HTML_DIRECTORY'],
        'TOKEN_DIRECTORY': args['TOKEN_DIRECTORY'],
        'STOPLIST': args['STOPLIST']
    })
    print "\tCompleted generating corpus from the raw html."
    __make_inverted_index__({
        'TOKEN_DIRECTORY': args['TOKEN_DIRECTORY'],
        'N_GRAM': args['N_GRAM']
    })
    print "\tCompleted generating inverted index for the corpus."
    __generate_corpus_statistics__({
        'BASE_DIRECTORY': args['BASE_DIRECTORY'],
        'N_GRAM': args['N_GRAM']
    })
    print "\tCreated term document frequency and term frequency text in {} for the inverted_index.".format(
        args['BASE_DIRECTORY'])
    __save_dict__({'BASE_DIRECTORY': args['BASE_DIRECTORY']})
    print "\tSaved the dict as pickle files in {} directory".format(
        args['BASE_DIRECTORY'])


# args: RAW_HTML_DIRECTORY, TOKEN_DIRECTORY, STOPLIST
def __make_corpus__(args):
    stopwords = []
    if args['STOPLIST']:
        stopwords = open(args['STOPLIST'], 'r').read().split()
    for filename in os.listdir(args['RAW_HTML_DIRECTORY']):
        __tokenize_file__({
            'RAW_HTML_DIRECTORY': args['RAW_HTML_DIRECTORY'],
            'FILENAME': filename,
            'TOKEN_DIRECTORY': args['TOKEN_DIRECTORY'],
            'STOPWORDS': stopwords
        })


# args: RAW_HTML_DIRECTORY, FILENAME, TOKEN_DIRECTORY, STOPWORDS
def __tokenize_file__(args):
    # Get contents of file
    file_contents = open(
        os.path.join(args['RAW_HTML_DIRECTORY'], args['FILENAME']), 'r').read()

    # Pre-Process file contents, just the content of the wiki
    soup = process_html({'HTML': file_contents})

    filename = os.path.splitext(args['FILENAME'])[0].translate(None,
                                                               "_-") + '.txt'
    text = soup.get_text()
    # remove unwanted digits at the end of the file
    text = re.sub(r"^\d+\t\d+\t\d+$", " ", text, flags=re.M)
    # remove URL's
    text = re.sub(r"http\S+", " ", text)
    # Pre-Process text and store in corpus
    text = process_text({'TEXT': text})
    if (args['STOPWORDS']):
        text_tokens = text.split()
        text_tokens = [x for x in text_tokens if x not in args['STOPWORDS']]
        text = ' '.join(text_tokens)
    open(os.path.join(args['TOKEN_DIRECTORY'], filename),
         'w').write(text.encode('utf-8'))


# args: HTML
def process_html(args):
    # Pre-Process file contents, just the content of the wiki
    soup = BeautifulSoup(args['HTML'], 'html.parser')
    # remove all script and style elements
    for html_tag in soup.findAll(["script", "style"]):
        html_tag.decompose()
    # TODO remove unnecessary contents from html
    return soup


# args: TEXT
def process_text(args):
    text = args['TEXT']
    # case folding
    text = text.lower()
    # TODO: should em-dash be replaced with "-"
    # remove all non printable characters
    text = re.sub(r"[^\x00-\x7f]", " ", text)
    # remove all string punctuations other than "-", ".", ","
    text = re.sub(r"[!\"#$%&\'()*+/:;<=>?@[\\\]^_`{|}~]", " ", text)
    # remove all "-" not between text
    text = re.sub(r"(?<![a-zA-Z0-9])-|-(?![a-zA-Z0-9])", " ", text)
    # remove all ",", "." in text not between digits
    text = re.sub(r"(?<!\d)[,.]|[,.](?!\d)", " ", text)
    # remove multiple \s+ characters
    # TODO post process text after examining contents
    text = ' '.join(text.split())
    return text


# args: TOKEN_DIRECTORY, N_GRAM
def __make_inverted_index__(args):
    for filename in os.listdir(args['TOKEN_DIRECTORY']):
        __create_inverted_index__({
            'TOKEN_DIRECTORY': args['TOKEN_DIRECTORY'],
            'FILENAME': filename,
            'N_GRAM': args['N_GRAM']
        })


# args: TOKEN_DIRECTORY, FILENAME, N_GRAM
def __create_inverted_index__(args):
    global __inverted_index__, __token_index__, __corpus_statistics__
    __corpus_statistics__['TOTAL_DOCUMENTS'] += 1
    tokens = open(
        os.path.join(args['TOKEN_DIRECTORY'], args['FILENAME']),
        'r').read().split()
    tokens = __find_ngrams__({'TOKENS': tokens, 'N_GRAM': args['N_GRAM']})
    documentid = os.path.splitext(args['FILENAME'])[0]
    document_length = len(tokens)
    __token_index__[documentid] = document_length
    __corpus_statistics__['CORPUS_LENGTH'] += document_length
    grouped_tokens = Counter(tokens)
    for token, frequency in grouped_tokens.iteritems():
        token = ' '.join(token)
        __inverted_index__[token][documentid] = frequency


# args: TOKENS, N_GRAM
def __find_ngrams__(args):
    return zip(*[args['TOKENS'][i:] for i in range(args['N_GRAM'])])


# args: BASE_DIRECTORY, N_GRAM
def __generate_corpus_statistics__(args):
    global __term_frequency__
    term_document_frequency = []
    term_document_frequency.append(['term', 'docID', 'df'])

    for term, document_frequencies in sorted(
            dict(__inverted_index__).iteritems()):

        term_document_frequency.append([
            term, ', '.join(sorted(document_frequencies.keys())),
            len(document_frequencies)
        ])
        __term_frequency__[term] = sum(document_frequencies.values())
    with open(
            os.path.join(args['BASE_DIRECTORY'], 'term_document_frequency_' +
                         str(args['N_GRAM']) + '_gram.txt'),
            'w') as term_document_frequency_file:
        term_document_frequency_file.write("\n".join("\t\t".join(map(
            str, l)) for l in term_document_frequency))

    term_frequency = []
    term_frequency.append(['term', 'tf'])
    for term in sorted(
            __term_frequency__, key=__term_frequency__.get, reverse=True):
        term_frequency.append([term, __term_frequency__[term]])
    with open(
            os.path.join(
                args['BASE_DIRECTORY'],
                'term_frequency_' + str(args['N_GRAM']) + '_gram.txt'),
            'w') as term_frequency_file:
        term_frequency_file.write(
            "\n".join("\t\t".join(map(str, l)) for l in term_frequency))


# args: BASE_DIRECTORY
def __save_dict__(args):
    pickle.dump(__token_index__,
                open(
                    os.path.join(args['BASE_DIRECTORY'], 'token_index.pkl'),
                    'wb'))
    pickle.dump(__inverted_index__,
                open(
                    os.path.join(args['BASE_DIRECTORY'], 'inverted_index.pkl'),
                    'wb'))
    pickle.dump(__corpus_statistics__,
                open(
                    os.path.join(args['BASE_DIRECTORY'],
                                 'corpus_statistics.pkl'), 'wb'))


#args: RAW_HTML_DIRECTORY, STOPLIST
def main(args):
    base_dir = os.path.dirname(args['RAW_HTML_DIRECTORY'])
    token_dir = os.path.join(base_dir, __token_directory__)
    try:
        os.makedirs(token_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
        pass
    print "Triggering inverted_index.\n\tCreated '{}' directory to save tokens.".format(
        token_dir)
    __generate_inverted_index__({
        'BASE_DIRECTORY':
        base_dir,
        'RAW_HTML_DIRECTORY':
        args['RAW_HTML_DIRECTORY'],
        'TOKEN_DIRECTORY':
        token_dir,
        'STOPLIST':
        args['STOPLIST'],
        'N_GRAM':
        __n_gram__
    })
