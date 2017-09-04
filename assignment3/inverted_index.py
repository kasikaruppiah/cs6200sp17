#!/usr/bin/python

# Implementing your own inverted indexer. Text processing and corpus statistics.

import math
import os
import re
import string
from collections import Counter, defaultdict

import matplotlib.pyplot as plt
import numpy as np
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
    for html_tag in soup.findAll(["script", "style", "sup", "sub", "table"]):
        html_tag.decompose()
    # remove [ edit ] links
    for span in soup.findAll("span", {'class': 'mw-editsection'}):
        span.decompose()
    # remove References div
    for div in soup.findAll("div", {'class': ['navbox', 'reflist']}):
        div.decompose()
    # remove toc div
    for div in soup.findAll("div", {'id': 'toc'}):
        div.decompose()

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
    text = re.sub(r"(?<![a-zA-Z0-9])-|-(?![a-zA-Z0-9])", " ", text)
    # remove all ",", "." in text not between digits
    text = re.sub(r"(?<![0-9])[,.]|[,.](?![0-9])", " ", text)
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


# args: BASE_DIRECTORY, N_GRAM
def __generate_zipfian_curve__(args):
    frequencies = __term_frequency__.values()
    log_frequencies = map(lambda f: math.log(f),
                          sorted(frequencies, key=int, reverse=True))
    total_tokens = sum(frequencies)
    probabilities = map(lambda f: f * 1.0 / total_tokens, frequencies)
    probabilities.sort(reverse=True)
    ranks = np.array(xrange(1, len(__term_frequency__) + 1))
    log_ranks = map(lambda r: math.log(r), ranks)

    zipfian_curve = plt.figure(figsize=(16, 6))
    zipfian_curve.suptitle(
        "Zipfian Curve - Word {}-Gram".format(args['N_GRAM'], y=1.05))
    probability_curve = zipfian_curve.add_subplot(121)
    probability_curve.set_title("Rank vs Probability")
    probability_curve.set_xlabel("Rank (by decreasing frequency)")
    probability_curve.set_ylabel("Probability (of occurrence)")
    probability_curve.plot(ranks, probabilities, 'r+', label='Wiki')
    probability_curve.legend(loc='upper right')
    frequency_curve = zipfian_curve.add_subplot(122)
    frequency_curve.set_title("Log Rank vs Log Frequency")
    frequency_curve.set_xlabel("log 10 rank")
    frequency_curve.set_ylabel("log 10 tf")
    frequency_curve.plot(log_ranks, log_frequencies, 'r+', label='Wiki')
    frequency_curve.legend(loc='upper right')
    zipfian_curve.tight_layout()
    zipfian_curve.subplots_adjust(top=0.85)
    zipfian_curve.savefig(
        os.path.join(args['BASE_DIRECTORY'],
                     'zipfian_curve_' + str(args['N_GRAM']) + '_gram.png'),
        format='png',
        dpi=300)
