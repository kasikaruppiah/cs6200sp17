#!/usr/bin/python

import argparse
from datetime import datetime
import logging
import os
import errno

startTime = datetime.now()

parser = argparse.ArgumentParser(description = 'This is a page rank script created for cs6200sp17, assignment2')
parser.add_argument('-i', '--inlinks-file', help = 'In-Link relationship file containing Graph', required = True)
parser.add_argument('-o', '--output-dir', default = datetime.now().strftime('%Y%m%d%H%M%S'), help = 'Output directory for the page rank output file', required = False)
parser.add_argument('-v', '--verbose', action = 'store_true', help = 'Increase output verbosity')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format = '%(levelname)s : %(funcName)s - %(message)s', level = logging.DEBUG)
else:
    logging.basicConfig(format = '%(levelname)s : %(funcName)s - %(message)s')

inlink_file = open(args.inlinks_file, 'r')

inlinks = {}
outlinks = {}
for line in inlink_file:
    document_ids = line.strip().split(' ')
    inlink_page = document_ids.pop(0)
    inlinks[inlink_page] = document_ids
    for document_id in document_ids:
        if document_id in outlinks:
            outlinks[document_id].append(inlink_page)
        else:
            outlinks[document_id] = [inlink_page]

pagerank = {}
for document_id in inlinks:
    pagerank[document_id] = 1.0 / len(inlinks)



print inlinks
print outlinks

'''
try:
    os.mkdir(args.output_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise e
    pass
os.chdir(args.output_dir)
print "Created '{0}' directory to save page rank results".format(args.output_dir)
'''
