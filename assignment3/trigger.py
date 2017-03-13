#!/usr/bin/python

import argparse
import errno
import os
from datetime import datetime

import generate_corpus
import pagerank
import webcrawler

HTML_DIRECTORY = 'raw_html'
TOKEN_DIRECTORY = 'tokens'

parser = argparse.ArgumentParser(
    description='This is a triggering script created for cs6200sp17')
parser.add_argument(
    '-o',
    '--output-dir',
    default=datetime.now().strftime('%Y%m%d%H%M%S'),
    help='Output directory for the downloaded web pages and links text',
    required=False)
parser.add_argument(
    '-s', '--seed-url', help='Starting URL for the crawler', required=False)
parser.add_argument(
    '-k',
    '--keyword',
    default=None,
    help='Keyword for focused crawling',
    required=False)
parser.add_argument(
    '-l',
    '--limit',
    type=int,
    default=1000,
    help='Maximum number of pages to be crawled, defaults to 1000',
    required=False)
parser.add_argument(
    '-d',
    '--depth',
    type=int,
    default=5,
    help='Level to be crawled, defaults to 5',
    required=False)
parser.add_argument(
    '-dfc',
    '--depth-first-crawl',
    action='store_true',
    default=False,
    help='Use Depth first search for crawling, defaults to False',
    required=False)
parser.add_argument(
    '-p',
    '--politeness',
    type=int,
    default=1,
    help='Seconds to wait between HTTP request, defaults to 1',
    required=False)
parser.add_argument(
    '-pr',
    '--pagerank',
    action='store_true',
    default=False,
    help='pagerank for in-link relationship, defaults to False',
    required=False)
parser.add_argument(
    '-i',
    '--in-link',
    default='in_link.txt',
    help='in-link relationship file to use to compute pagerank, defaults to in_link.txt',
    required=False)
parser.add_argument(
    '-c',
    '--convergence',
    type=float,
    default=1,
    help='Diff of perplexity value to be considered for convergence, defaults to 1',
    required=False)
parser.add_argument(
    '-itr',
    '--iterations',
    type=int,
    default=4,
    help='Iterations to check for convergence, defaults to 4',
    required=False)
parser.add_argument(
    '-gc',
    '--generate-corpus',
    action='store_true',
    default=False,
    help='generate corpus from raw html files, defaults to False',
    required=False)
parser.add_argument(
    '-rhd',
    '--raw-html-directory',
    default='raw_html',
    help='raw html file directory, defaults to raw_html',
    required=False)
args = parser.parse_args()

startTime = datetime.now()

if args.seed_url:
    try:
        os.mkdir(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
        pass
    print "Created '{}' directory to save script results.".format(
        args.output_dir)
else:
    if not os.path.isdir(args.output_dir):
        raise Exception(
            "can't open '{}': No such directory".format(args.output_dir))

if args.seed_url:
    try:
        os.mkdir(os.path.join(args.output_dir, HTML_DIRECTORY))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
        pass
    print "Triggering webcrawler.\n\tCreated '{}' directory to save raw html.".format(
        HTML_DIRECTORY)
    webcrawler.crawl({
        'BASE_DIRECTORY': args.output_dir,
        'DEPTH': args.depth,
        'DEPTH_FIRST_CRAWL': args.depth_first_crawl,
        'KEYWORD': args.keyword,
        'LIMIT': args.limit,
        'POLITENESS': args.politeness,
        'SEED_URL': args.seed_url
    })

if args.pagerank:
    in_link_file_path = os.path.join(args.output_dir, args.in_link)
    if os.path.isfile(in_link_file_path):
        print "Triggering pagerank."
        pagerank.generate_pagerank({
            'BASE_DIRECTORY': args.output_dir,
            'CONVERGENCE': args.convergence,
            'IN_LINK_FILE': args.in_link,
            'ITERATIONS': args.iterations
        })
    else:
        raise Exception(
            "can't open '{}': No such file".format(in_link_file_path))

if args.generate_corpus:
    raw_html_directory_path = os.path.join(args.output_dir,
                                           args.raw_html_directory)
    if os.path.isdir(raw_html_directory_path):
        # TODO: Call generate_corpus after completion of function
        try:
            os.makedirs(os.path.join(args.output_dir, TOKEN_DIRECTORY))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e
            pass
        generate_corpus.make_corpus({
            'BASE_DIRECTORY':
            args.output_dir,
            'RAW_HTML_DIRECTORY':
            args.raw_html_directory,
            'TOKEN_DIRECTORY':
            TOKEN_DIRECTORY,
        })
    else:
        raise Exception("can't open '{}': No such directory".format(
            raw_html_directory_path))

print "Completed in {} seconds.".format(datetime.now() - startTime)
