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


# args: BASE_DIRECTORY, STEM_FILELOCATION, TOKEN_DIRECTORY, N_GRAM
def __generate_inverted_index__(args):
    __make_corpus__({
        'STEM_FILELOCATION': args['STEM_FILELOCATION'],
        'TOKEN_DIRECTORY': args['TOKEN_DIRECTORY']
    })
    print "\tCompleted generating corpus from the stem file."
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


# args: STEM_FILELOCATION, TOKEN_DIRECTORY
def __make_corpus__(args):
    file_contents = open(args['STEM_FILELOCATION'], 'r').read()
    corpus = re.split(r"^# \d+$", file_contents, flags=re.M)
    for index, corpora in enumerate(corpus[1:]):
        filename = 'CACM{:04d}.txt'.format(index + 1)
        open(os.path.join(args['TOKEN_DIRECTORY'], filename),
             'w').write(' '.join(corpora.split()).encode('utf-8'))


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


#args: STEM_FILELOCATION
def main(args):
    base_dir = os.path.dirname(args['STEM_FILELOCATION'])
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
        'STEM_FILELOCATION':
        args['STEM_FILELOCATION'],
        'TOKEN_DIRECTORY':
        token_dir,
        'N_GRAM':
        __n_gram__
    })
