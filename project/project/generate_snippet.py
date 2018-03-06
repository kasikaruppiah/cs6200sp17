#!/usr/bin/python

# bm25 ranking

from __future__ import division

import cPickle as pickle
import math
import os
import re
from collections import Counter, defaultdict

from bs4 import BeautifulSoup

import inverted_index
import Start_Dialog

__inverted_index__ = defaultdict(dict)
__token_index__ = {}
__corpus_statistics__ = {}
__bm25_score__ = {}
__base_directory__ = '../project_files/'
__html_directory__ = 'cacm'
__token_index_filename__ = os.path.join(__base_directory__, 'token_index.pkl')
__inverted_index_filename__ = os.path.join(__base_directory__,
                                           'inverted_index.pkl')
__corpus_statistics_filename__ = os.path.join(__base_directory__,
                                              'corpus_statistics.pkl')


# args: QUERY_STRING
def generate_snippet_html(args):
    global __bm25_score__
    __load_inverted_index__()
    query_string = inverted_index.process_text({'TEXT': args['QUERY_STRING']})
    __bm25_score__ = {}
    __bm25__({'QUERY_STRING': query_string})
    documentids = sorted(
        __bm25_score__, key=__bm25_score__.get, reverse=True)[:10]
    snippet_html = generate_html({
        'BASE_DIRECTORY': __base_directory__,
        'DOCUMENTIDS': documentids,
        'QUERY_STRING': query_string
    })
    Start_Dialog.DisplayResult(args['QUERY_STRING'], snippet_html)


def __load_inverted_index__():
    global __inverted_index__, __token_index__, __corpus_statistics__
    __inverted_index__ = pickle.load(open(__inverted_index_filename__, "rb"))
    __token_index__ = pickle.load(open(__token_index_filename__, "rb"))
    __corpus_statistics__ = pickle.load(
        open(__corpus_statistics_filename__, "rb"))


# args: QUERY_STRING
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


# args: BASE_DIRECTORY, DOCUMENTIDS, QUERY_STRING
def generate_html(args):
    snippet_html = ''
    if args['DOCUMENTIDS']:
        for document in args['DOCUMENTIDS']:
            html_filename = re.sub(r'(\d+)', r'-\1.html', document)
            snippet_html += __generate_snippet_from_file__({
                'FILELOCATION':
                os.path.join(args['BASE_DIRECTORY'], __html_directory__,
                             html_filename),
                'QUERIES':
                args['QUERY_STRING'].split()
            })
    else:
        snippet_html = "<br><br>Your search - <b>%s</b> - did not match any documents." % args[
            'QUERY_STRING'] \
        + "<br><br>Suggestions:<br><br>" \
        + "<ul><li>Make sure all words are spelled correctly.</li>" \
        + "<li>Try different keywords.</li>" + "<li>Try more general keywords.</li></ul>"
    return snippet_html


# args: FILELOCATION, QUERIES
def __generate_snippet_from_file__(args):
    file_contents = inverted_index.process_html({
        'HTML':
        open(args['FILELOCATION'], 'r').read()
    }).get_text()
    lines = re.split(r"(?<!\d)[.]|[.](?!\d)", file_contents, flags=re.M)
    snippet = 0
    score = 0
    for index, value in enumerate(lines):
        text = value
        # case folding
        text = text.lower()
        # remove all non printable characters
        text = re.sub(r"[^\x00-\x7f]", " ", text)
        # remove all string punctuations other than "-", ".", ","
        text = re.sub(r"[!\"#$%&\'()*+/:;<=>?@[\\\]^_`{|}~]", " ", text)
        # remove all "-" not between text
        text = re.sub(r"(?<![a-zA-Z0-9])-|-(?![a-zA-Z0-9])", " ", text)
        # remove all ",", "." in text not between digits
        text = re.sub(r"(?<!\d)[,.]|[,.](?!\d)", " ", text)
        # replace multiple spaces
        text = ' '.join(text.split())
        if text:
            line_score = math.pow(
                len(
                    re.findall(
                        r'\b(%s)\b' % '|'.join(args['QUERIES']),
                        text,
                        flags=re.I)), 2) / len(re.findall(r'\b\w+\b', text))
            if line_score > score:
                snippet = index
                score = line_score

    html_snippet = re.sub(
        r'\b(%s)\b' % '|'.join(args['QUERIES']),
        r'<b>\1</b>',
        lines[snippet],
        flags=re.I)
    html_snippet = '<u><b>%s</b></u><br>' % os.path.basename(
        args['FILELOCATION']) + html_snippet + '<br><br>'

    return html_snippet
