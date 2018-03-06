#!/usr/bin/python

import argparse
import os
from datetime import datetime

import bm25_ranking
import inverted_index
import stemmed_inverted_index
import tfidf_ranking

parser = argparse.ArgumentParser(
    description='This is a triggering script created for cs6200sp17')
parser.add_argument(
    '-i',
    '--create-inverted-index',
    action='store_true',
    default=False,
    help='Create inverted index from raw html, defaults to False',
    required=False)
parser.add_argument(
    '-stem',
    '--create-inverted-index-from-stem',
    action='store_true',
    default=False,
    help='Create inverted index from stem file, defaults to False',
    required=False)
parser.add_argument(
    '-s',
    '--stoplist',
    action='store_true',
    default=False,
    help='Create inverted index from raw html using stoplist, defaults to False',
    required=False)
parser.add_argument(
    '-b',
    '--bm25-ranking',
    action='store_true',
    default=False,
    help='Run bm25-ranking on inverted index, defaults to False',
    required=False)
parser.add_argument(
    '-t',
    '--tfidf-ranking',
    action='store_true',
    default=False,
    help='Run tfidf-ranking on inverted index, defaults to False',
    required=False)
parser.add_argument(
    '-e',
    '--expand-query',
    action='store_true',
    default=False,
    help='Expand query before ranking, defaults to False',
    required=False)
parser.add_argument(
    '-stem-query',
    '--stem-ranking',
    action='store_true',
    default=False,
    help='Run ranking using stem query file, defaults to False',
    required=False)
args = parser.parse_args()

startTime = datetime.now()

if args.create_inverted_index:
    # trigger inverted_index
    raw_html_directory = raw_input(
        "Enter full path of the raw html directory:")
    if os.path.isdir(raw_html_directory):
        stoplist = ''
        if args.stoplist:
            stoplist = raw_input("Enter full path of the stop list file:")
            if not os.path.isfile(stoplist):
                raise Exception(
                    "can't open '{}': No such directory".format(stoplist))
        inverted_index.main({
            'RAW_HTML_DIRECTORY': raw_html_directory,
            'STOPLIST': stoplist
        })
    else:
        raise Exception(
            "can't open '{}': No such directory".format(raw_html_directory))

if args.create_inverted_index_from_stem:
    # trigger inverted_index
    stemfile = raw_input("Enter full path of the stem file:")
    if os.path.isfile(stemfile):
        stemmed_inverted_index.main({'STEM_FILELOCATION': stemfile})
    else:
        raise Exception(
            "can't open '{}': No such directory".format(raw_html_directory))

if args.bm25_ranking or args.tfidf_ranking:
    base_directory = raw_input("Enter full path of the base directory:")
    if os.path.isdir(base_directory):
        query_file_location = ''
        stem_query_file_location = ''
        if args.stem_ranking:
            stem_query_file_location = raw_input(
                "Enter full path of the stem query file:")
            if not os.path.isfile(stem_query_file_location):
                raise Exception("can't open '{}': No such directory".format(
                    stem_query_file_location))
        else:
            query_file_location = raw_input(
                "Enter full path of the query file:")
            if not os.path.isfile(query_file_location):
                raise Exception("can't open '{}': No such directory".format(
                    query_file_location))
        file_ext = raw_input(
            "Enter a keyword for file naming (Optional, Blank if not required):"
        )
        if args.bm25_ranking:
            relevance_file_location = raw_input(
                "Enter full path of the relevance file:")
            if not os.path.isfile(relevance_file_location):
                raise Exception("can't open '{}': No such directory".format(
                    relevance_file_location))
            bm25_ranking.generate_bm25({
                'BASE_DIRECTORY':
                base_directory,
                'FILELOCATION':
                query_file_location,
                'STEM_FILELOCATION':
                stem_query_file_location,
                'RELEVANCE_FILELOCATION':
                relevance_file_location,
                'FILE_EXT':
                file_ext,
                'EXPAND_QUERY':
                args.expand_query
            })
        else:
            tfidf_ranking.generate_tfidf({
                'BASE_DIRECTORY':
                base_directory,
                'FILELOCATION':
                query_file_location,
                'STEM_FILELOCATION':
                stem_query_file_location,
                'FILE_EXT':
                file_ext,
                'EXPAND_QUERY':
                args.expand_query
            })
    else:
        raise Exception(
            "can't open '{}': No such directory".format(token_directory))

print "Completed in {} seconds.".format(datetime.now() - startTime)
