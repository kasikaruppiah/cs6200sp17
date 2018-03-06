#!/usr/bin/python

# tfidf ranking

from __future__ import division

import cPickle as pickle
import getpass
import math
import os
from collections import defaultdict

import cacm_query
import generate_snippet
import inverted_index
import Thesaurus

__inverted_index__ = defaultdict(dict)
__token_index__ = {}
__corpus_statistics__ = {}
__tfidf_score__ = {}
__token_index_filename__ = 'token_index.pkl'
__inverted_index_filename__ = 'inverted_index.pkl'
__corpus_statistics_filename__ = 'corpus_statistics.pkl'


# args: BASE_DIRECTORY, FILELOCATION, STEM_FILELOCATION
def generate_tfidf(args):
    global __tfidf_score__
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
    for query_id in sorted(query_strings.keys(), key=lambda x: int(x)):
        __tfidf_score__ = {}
        query_string = inverted_index.process_text({
            'TEXT':
            query_strings[query_id]
        })
        origional_query_string = query_string
        if args['EXPAND_QUERY']:
            query_string = ' ' + Thesaurus.GetSimilarNames(query_string)
        __tfidf__({'QUERY_STRING': query_string})
        tfidf_scores = []
        tfidf_scores.append(
            ['query_id', 'Q0', 'doc_id', 'rank', 'tfidf_score', 'system_name'])
        rank = 0
        documentids = sorted(
            __tfidf_score__, key=__tfidf_score__.get, reverse=True)[:100]
        for documentid in documentids:
            rank += 1
            tfidf_scores.append([
                query_id, 'Q0', documentid, rank, __tfidf_score__[documentid],
                username
            ])
        filename = 'tfidf_'
        if args['FILE_EXT']:
            filename += '%s_' % args['FILE_EXT']
        filename += 'query_%s.txt' % query_id
        with open(os.path.join(args['BASE_DIRECTORY'], filename),
                  'w') as tfidf_file:
            tfidf_file.write(
                "\n".join("\t\t".join(map(str, l)) for l in tfidf_scores))
        filename = os.path.splitext(filename)[0] + '.html'
        with open(os.path.join(args['BASE_DIRECTORY'], filename),
                  'w') as snippet_file:
            snippet_html = generate_snippet.generate_html({
                'BASE_DIRECTORY':
                args['BASE_DIRECTORY'],
                'DOCUMENTIDS':
                documentids[:10],
                'QUERY_STRING':
                origional_query_string
            })
            snippet_html = '<b>tf-idf</b><br><br>Query - <b>%s</b><br><br>' % query_strings[
                query_id] + snippet_html
            snippet_file.write(snippet_html)
        print "\t\tProcessed query {}".format(query_id)

    print "\tSaved query results in {} directory".format(
        args['BASE_DIRECTORY'])


# args: BASE_DIRECTORY
def __load_inverted_index__(args):
    global __inverted_index__, __token_index__, __corpus_statistics__
    __inverted_index__ = pickle.load(
        open(
            os.path.join(args['BASE_DIRECTORY'], __inverted_index_filename__),
            "rb"))
    __token_index__ = pickle.load(
        open(
            os.path.join(args['BASE_DIRECTORY'], __token_index_filename__),
            "rb"))
    __corpus_statistics__ = pickle.load(
        open(
            os.path.join(args['BASE_DIRECTORY'],
                         __corpus_statistics_filename__), "rb"))


# args: QUERY_STRING
def __tfidf__(args):
    global __tfidf_score__

    queries = args['QUERY_STRING'].split()
    N = __corpus_statistics__['TOTAL_DOCUMENTS']

    for term in queries:
        if term in __inverted_index__:
            n = len(__inverted_index__[term])
            for documentid, frequency in dict(
                    __inverted_index__[term]).iteritems():
                tf = frequency / __token_index__[documentid]
                idf = math.log(N / n)
                __tfidf_score__[documentid] = __tfidf_score__.get(
                    documentid, 0.0) + (tf * idf)
