#!/usr/bin/python

# Implementing your own inverted indexer. Text processing and corpus statistics.
import os
import re
import string
from collections import Counter, defaultdict

import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

__inverted_index__ = defaultdict(dict)
__token_index__ = {}
__term_frequency__ = {}


# args: BASE_DIRECTORY, RAW_HTML_DIRECTORY, TOKEN_DIRECTORY, N_GRAM
def generate_inverted_index(args):
    raw_html_directory = os.path.join(args['BASE_DIRECTORY'],
                                      args['RAW_HTML_DIRECTORY'])
    token_directory = os.path.join(args['BASE_DIRECTORY'],
                                   args['TOKEN_DIRECTORY'])
    __make_corpus__({
        'RAW_HTML_DIRECTORY': raw_html_directory,
        'TOKEN_DIRECTORY': token_directory
    })
    print "\tCompleted generating corpus for the raw html."
    __make_inverted_index__({
        'TOKEN_DIRECTORY': token_directory,
        'N_GRAM': args['N_GRAM']
    })
    print "\tCompleted generating inverted index for the corpus."
    __generate_corpus_statistics__({
        'BASE_DIRECTORY': args['BASE_DIRECTORY'],
        'N_GRAM': args['N_GRAM']
    })
    print "\tCreated term document frequency and term frequency text in {} for the inverted_index.".format(
        args['BASE_DIRECTORY'])
    __generate_zipfian_curve__({
        'BASE_DIRECTORY': args['BASE_DIRECTORY'],
        'N_GRAM': args['N_GRAM']
    })
    print "\tCreated zipfian curve in {} for the inverted index.".format(
        args['BASE_DIRECTORY'])


# args: BASE_DIRECTORY, RAW_HTML_DIRECTORY, TOKEN_DIRECTORY
def __make_corpus__(args):
    for filename in os.listdir(args['RAW_HTML_DIRECTORY']):
        __tokenize_file__({
            'RAW_HTML_DIRECTORY': args['RAW_HTML_DIRECTORY'],
            'FILENAME': filename,
            'TOKEN_DIRECTORY': args['TOKEN_DIRECTORY']
        })


# args: RAW_HTML_DIRECTORY, FILENAME, TOKEN_DIRECTORY
def __tokenize_file__(args):
    # Get contents of file
    file_contents = open(
        os.path.join(args['RAW_HTML_DIRECTORY'], args['FILENAME']), 'r').read()

    # Pre-Process file contents, just the content of the wiki
    soup = BeautifulSoup(file_contents, 'html.parser').find(
        'div', id='content')

    # remove all script and style elements
    for html_tag in soup(["script", "style"]):
        html_tag.extract()
    # remove all html tags
    text = soup.get_text()
    # remove URL's
    text = re.sub(r"http\S+", " ", text)
    # case folding
    text = text.lower()
    # TODO: should em-dash be replaced with "-"
    # remove all non printable characters
    text = re.sub(r"[^\x00-\x7f]", " ", text)
    # remove all string punctuations other than "-", ".", ","
    text = re.sub(r"[!\"#$%&\'()*+/:;<=>?@[\\\]^_`{|}~]", " ", text)
    # remove all "-" not between text
    # TODO: improve efficiency - find alternative to |
    text = re.sub(r"(?<![a-zA-Z0-9])-|-(?![a-zA-Z0-9])", " ", text)
    # remove all ,", "." in text not between digits

    # remove multiple \s+ characters
    text = ' '.join(text.split())

    filename = args['FILENAME'].translate(None, "_-") + '.txt'
    open(os.path.join(args['TOKEN_DIRECTORY'], filename),
         'w').write(text.encode('utf-8'))


# args: BASE_DIRECTORY, TOKEN_DIRECTORY, N_GRAM
def __make_inverted_index__(args):
    for filename in os.listdir(args['TOKEN_DIRECTORY']):
        __create_inverted_index__({
            'TOKEN_DIRECTORY': args['TOKEN_DIRECTORY'],
            'FILENAME': filename,
            'N_GRAM': args['N_GRAM']
        })


# args: TOKEN_DIRECTORY, FILENAME, N_GRAM
def __create_inverted_index__(args):
    global __inverted_index__, __token_index__
    tokens = __find_ngrams__({
        'TOKENS':
        open(os.path.join(args['TOKEN_DIRECTORY'], args['FILENAME']),
             'r').read().split(),
        'N_GRAM':
        args['N_GRAM']
    })
    documentid = os.path.splitext(args['FILENAME'])[0]
    __token_index__[documentid] = len(tokens)
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
    term_document_frequency_text = "term\tdocID\tdf\n"
    for term, document_frequencies in sorted(dict(__inverted_index__).items()):
        term_total_frequency = 0
        for documentid, frequency in sorted(document_frequencies.items()):
            term_document_frequency_text += "{}\t{}\t{}\n".format(
                term, documentid, frequency)
            term_total_frequency += frequency
        __term_frequency__[term] = term_total_frequency
    term_frequency_text = "term\ttf\n"
    for term in sorted(
            __term_frequency__, key=__term_frequency__.get, reverse=True):
        term_frequency_text += "{}\t{}\n".format(term,
                                                    __term_frequency__[term])
    with open(
            os.path.join(args['BASE_DIRECTORY'], 'term_document_frequency_' +
                         str(args['N_GRAM']) + '_gram.txt'),
            'w') as term_document_frequency_file:
        term_document_frequency_file.write(term_document_frequency_text)
    with open(
            os.path.join(args['BASE_DIRECTORY'], 'term_frequency_' +
                         str(args['N_GRAM']) + '_gram.txt'),
            'w') as term_frequency_file:
        term_frequency_file.write(term_frequency_text)


# args: BASE_DIRECTORY, N_GRAM
def __generate_zipfian_curve__(args):
    token_size = len(__term_frequency__)
    frequencies = __term_frequency__.values()
    total_tokens = sum(frequencies)
    probabilities = map(lambda f: f * 1.0 / total_tokens, frequencies)
    probabilities.sort(reverse=True)
    rank_probability = [(rank + 1, probability)
                        for rank, probability in enumerate(probabilities)]
    ranks, probs = zip(*rank_probability)
    plt.xscale('linear')
    plt.xscale('linear')
    plt.title("Zipfian Curve - Word {}-Gram".format(args['N_GRAM']))
    plt.xlabel("Rank (by decreasing frequency)")
    plt.ylabel("Probability (of occurrence)")
    plt.plot([1, token_size], [0.1, 0.1 / token_size], label='Expected')
    plt.plot(ranks, probs, 'r+', label='Actual')
    plt.legend(loc='upper right')
    plt.savefig(
        os.path.join(args['BASE_DIRECTORY'], 'zipfian_curve_' + str(args[
            'N_GRAM']) + '_gram.png'))
