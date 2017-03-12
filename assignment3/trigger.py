#!/usr/bin/python

import argparse
import errno
import os
from datetime import datetime

import pagerank
import webcrawler

HTML_DIRECTORY = 'raw_html'

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
    help='pagerank for in-link relationship',
    required=False)
parser.add_argument(
    '-i',
    '--in-link',
    default='in_link.txt',
    help='in-link relationship file to use to compute pagerank',
    required=False)
parser.add_argument(
    '-c',
    '--convergence',
    type=int,
    default=1,
    help='Diff of perplexity value to be considered for convergence',
    required=False)
parser.add_argument(
    '-d',
    '--iterations',
    type=int,
    default=4,
    help='Iterations to check for convergence',
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
    print "Triggering pagerank."
    pagerank.generate_pagerank({
        'BASE_DIRECTORY': args.output_dir,
        'CONVERGENCE': args.convergence,
        'IN_LINK_FILE': args.in_link,
        'ITERATIONS': args.iterations
    })

print "Completed in {} seconds.".format(datetime.now() - startTime)
