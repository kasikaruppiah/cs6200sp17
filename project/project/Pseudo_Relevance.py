#!/usr/bin/python

# bm25 ranking

from __future__ import division

import cPickle as pickle
import getpass
import math
import os
from collections import Counter, defaultdict

import cacm_query
import inverted_index
import Thesaurus

__inverted_index__ = defaultdict(dict)
__token_index__ = {}
__corpus_statistics__ = {}
__bm25_score__ = {}
__relevance__ = {}
__token_index_filename__ = 'token_index.pkl'
__inverted_index_filename__ = 'inverted_index.pkl'
__corpus_statistics_filename__ = 'corpus_statistics.pkl'
__pseudo_relevance__ = {}


# args: BASE_DIRECTORY, FILELOCATION, STEM_FILELOCATION, RELEVANCE_FILELOCATION, RELEVANCE_FILELOCATION, FILE_EXT
def generate_bm25(args):
    global __bm25_score__
    __load_inverted_index__({'BASE_DIRECTORY': args['BASE_DIRECTORY']})
    print "\tCompleted loading inverted index from pickle files."
    username = getpass.getuser()
    query_strings = {}
    fileLocation = args['FILELOCATION']
    if fileLocation:
        query_strings = cacm_query.get_queries({'FILELOCATION': fileLocation})
    else:
        querylist = open(args['STEM_FILELOCATION']).readlines()
        i = 1
        for query in querylist:
            query_strings[str(i)] = query.strip()
            i += 1
    relevanceFileLocation = args['RELEVANCE_FILELOCATION']
    if relevanceFileLocation:
        __load_relevance_data__({
            'RELEVANCE_FILELOCATION': relevanceFileLocation
        })
    for query_id in sorted(query_strings.keys(), key=lambda x: int(x)):
        __bm25_score__ = {}
        query_string = inverted_index.process_text({
            'TEXT':
            query_strings[query_id]
        })
        if args['EXPAND_QUERY']:
            __bm25__({'QUERY_STRING': query_string, 'QUERY_ID': query_id})
            for documentid in sorted(
                    __bm25_score__, key=__bm25_score__.get, reverse=True)[:20]:
                docLines = open(
                    os.path.join(args['BASE_DIRECTORY'], 'corpus',
                                 documentid + ".txt"), 'r').read()
                for word in docLines.split():
                    if word not in __pseudo_relevance__:
                        __pseudo_relevance__[word] = 1
                    else:
                        __pseudo_relevance__[word] += 1
            query_string += ' ' + ' '.join(
                sorted(
                    __pseudo_relevance__,
                    key=__pseudo_relevance__.get,
                    reverse=True)[:20])
            __bm25_score__ = {}
        __bm25__({'QUERY_STRING': query_string, 'QUERY_ID': query_id})
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

        filename = 'bm25_'
        fileExtension = args['FILE_EXT']
        if fileExtension:
            filename += '%s_' % fileExtension
        filename += 'query_%s.txt' % query_id
        with open(os.path.join(args['BASE_DIRECTORY'], filename),
                  'w') as bm25_file:
            bm25_file.write(
                "\n".join("\t\t".join(map(str, l)) for l in bm25_scores))
        print "\t\tProcessed query {}".format(query_id)

    print "\tSaved query results in {} directory".format(
        args['BASE_DIRECTORY'])


# args: BASE_DIRECTORY
def __load_inverted_index__(args):
    global __inverted_index__, __token_index__, __corpus_statistics__
    baseDirectory = args['BASE_DIRECTORY']
    __inverted_index__ = pickle.load(
        open(os.path.join(baseDirectory, __inverted_index_filename__), "rb"))
    __token_index__ = pickle.load(
        open(os.path.join(baseDirectory, __token_index_filename__), "rb"))
    __corpus_statistics__ = pickle.load(
        open(
            os.path.join(baseDirectory, __corpus_statistics_filename__), "rb"))


# args: RELEVANCE_FILELOCATION
def __load_relevance_data__(args):
    global __relevance__
    relevance_datas = open(args['RELEVANCE_FILELOCATION'], 'r').readlines()
    for relevance_data in relevance_datas:
        relevance_info = relevance_data.split()
        docids = relevance_info[2].split("-")
        docids[1] = '{:04d}'.format(int(docids[1]))
        docid = ''.join(docids)
        if relevance_info[0] in __relevance__:
            __relevance__[relevance_info[0]][docid] = 1
        else:
            __relevance__[relevance_info[0]] = {docid: 1}


# args: QUERY_STRING, QUERY_ID
def __bm25__(args):
    global __bm25_score__

    queries = args['QUERY_STRING'].split()
    grouped_query = Counter(queries)

    R = 0
    r = 0
    N = __corpus_statistics__['TOTAL_DOCUMENTS']
    k1 = 1.2
    k2 = 100.0
    b = 0.75
    avdl = __corpus_statistics__['CORPUS_LENGTH'] / N

    for term in queries:
        if term in __inverted_index__:
            n = len(__inverted_index__[term])

            for documentid, frequency in dict(
                    __inverted_index__[term]).iteritems():
                K = k1 * ((1 - b) + (b * __token_index__[documentid] / avdl))
                bm25 = (math.log(((r + 0.5) / (R - r + 0.5)) / (
                    (n - r + 0.5) / (N - n - R + r + 0.5))) * ((
                        (k1 + 1.0) * frequency) / (K + frequency)) *
                        (((k2 + 1.0) * grouped_query[term]) /
                         (k2 + grouped_query[term])))
                __bm25_score__[documentid] = __bm25_score__.get(documentid,
                                                                0.0) + bm25
