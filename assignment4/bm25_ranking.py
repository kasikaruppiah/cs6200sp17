#!/usr/bin/python

# Implementing your own inverted indexer. Text processing and corpus statistics.

from __future__ import division

import errno
import getpass
import math
import os
from collections import Counter, defaultdict

__inverted_index__ = defaultdict(dict)
__token_index__ = {}
__total_tokens__ = 0
__bm25_score__ = {}


# args: BASE_DIRECTORY, RAW_HTML_DIRECTORY, TOKEN_DIRECTORY, N_GRAM
def generate_bm25(args):
    global __bm25_score__
    __make_inverted_index__({
        'TOKEN_DIRECTORY': args['TOKEN_DIRECTORY'],
        'N_GRAM': args['N_GRAM']
    })
    print "\tCompleted generating inverted index for the corpus."

    query_string = raw_input("Enter the search query (q=quit):")
    query_id = 0
    username = getpass.getuser()
    while (query_string != 'q'):
        __bm25_score__ = {}

        __bm25__({'QUERY_STRING': query_string})

        query_id += 1
        bm25_scores = []
        bm25_scores.append(
            ['query_id', 'Q0', 'doc_id', 'rank', 'BM25_score', 'system_name'])
        rank = 0
        for documentid in sorted(
                __bm25_score__, key=__bm25_score__.get, reverse=True)[:100]:
            rank += 1
            bm25_scores.append([
                query_id, 'Q0', documentid, rank, __bm25_score__[documentid],
                username
            ])

        with open('bm25_' + "_".join(query_string.split()) + '.txt',
                  'w') as bm25_file:
            bm25_file.write(
                "\n".join("\t\t".join(map(str, l)) for l in bm25_scores))
        query_string = raw_input("Enter the search query (q=quit):")
    print "\tSaved results in current directory"


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
    global __inverted_index__, __token_index__, __total_tokens__
    tokens = __find_ngrams__({
        'TOKENS':
        open(os.path.join(args['TOKEN_DIRECTORY'], args['FILENAME']),
             'r').read().split(),
        'N_GRAM':
        args['N_GRAM']
    })
    documentid = os.path.splitext(args['FILENAME'])[0]
    document_length = len(tokens)
    __token_index__[documentid] = document_length
    __total_tokens__ += document_length
    grouped_tokens = Counter(tokens)
    for token, frequency in grouped_tokens.iteritems():
        token = ' '.join(token)
        __inverted_index__[token][documentid] = frequency


# args: TOKENS, N_GRAM
def __find_ngrams__(args):
    return zip(*[args['TOKENS'][i:] for i in range(args['N_GRAM'])])


def __bm25__(args):
    global __bm25_score__

    queries = args['QUERY_STRING'].split()
    grouped_query = Counter(queries)

    r = 0.0
    R = 0.0
    N = 1000.0
    k1 = 1.2
    k2 = 100.0
    b = 0.75
    avdl = __total_tokens__ / 1000.0

    for term in queries:
        n = len(__inverted_index__.get(term, []))
        for documentid, frequency in dict(
                __inverted_index__.get(term)).iteritems():
            K = k1 * ((1 - b) + (b * __token_index__[documentid] / avdl))
            bm25 = (math.log(((r + 0.5) / (R - r + 0.5)) / (
                (n - r + 0.5) / (N - n - R + r + 0.5))) * ((
                    (k1 + 1.0) * frequency) / (K + frequency)) *
                    (((k2 + 1.0) * grouped_query[term]) /
                     (k2 + grouped_query[term])))
            __bm25_score__[documentid] = __bm25_score__.get(documentid,
                                                            0.0) + bm25


token_directory = raw_input("Enter full path of the token directory:")
if os.path.isdir(token_directory):
    generate_bm25({'TOKEN_DIRECTORY': token_directory, 'N_GRAM': 1})
else:
    raise Exception("can't open '{}': No such directory".format(token_directory
))
