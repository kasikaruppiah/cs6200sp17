#!/usr/bin/python

import argparse
from datetime import datetime
import logging
import math
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
inlinks_count = {}
outlinks = {}
for line in inlink_file:
    document_ids = line.strip().split(' ')
    inlink_page = document_ids.pop(0)
    inlinks[inlink_page] = document_ids
    inlinks_count[inlink_page] = len(document_ids)
    for document_id in document_ids:
        if document_id in outlinks:
            outlinks[document_id].append(inlink_page)
        else:
            outlinks[document_id] = [inlink_page]

total_pages = len(inlinks)
sink_pages = []
for x in inlinks:
    if x not in outlinks:
        sink_pages.append(x)
print "Total Pages : {0}\nPages with no out-links : {1}".format(total_pages, len(sink_pages))
damping_factor = 0.85

pagerank = {}
new_pagerank = {}
for document_id in inlinks:
    pagerank[document_id] = 1.0 / total_pages

preplexity_rank = []
index = 0;

preplexity = 0
old_preplexity = 0

shannon_entropy = 0
for page in inlinks:
    shannon_entropy += pagerank[page] * math.log(pagerank[page], 2)
old_preplexity = 2 ** -shannon_entropy
preplexity_rank.append(old_preplexity)

while index < 4:
    sink_pagerank = 0
    for page in sink_pages:
        sink_pagerank += pagerank[page]
    for page in inlinks:
        new_pagerank[page] = (1 - damping_factor) / total_pages
        new_pagerank[page] += damping_factor * sink_pagerank / total_pages
        for inlink_page in inlinks[page]:
            new_pagerank[page] += damping_factor * pagerank[inlink_page] / len(outlinks[inlink_page])
    for page in inlinks:
        pagerank[page] = new_pagerank[page]

    shannon_entropy = 0
    for page in inlinks:
        shannon_entropy += pagerank[page] * math.log(pagerank[page], 2)
    preplexity = 2 ** -shannon_entropy
    preplexity_rank.append(preplexity)
    if (abs(preplexity - old_preplexity) < 1):
        index += 1
    else:
        index = 0
    old_preplexity = preplexity

try:
    os.mkdir(args.output_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise e
    pass
os.chdir(args.output_dir)
print "Created '{0}' directory to save page rank results".format(args.output_dir)

with open('inlinks_count.txt', 'w') as inlinks_file:
    inlinks_text = ''
    for key in sorted(inlinks_count, key=inlinks_count.get, reverse=True):
        inlinks_text += "{0}\t:\t{1}\n".format(key, inlinks_count[key])
    inlinks_file.write(inlinks_text)

with open('pagerank.txt', 'w') as pagerank_file:
    pagerank_text = ''
    for key in sorted(pagerank, key=pagerank.get, reverse=True):
        pagerank_text += "{0}\t:\t{1}\n".format(key, pagerank[key])
    pagerank_file.write(pagerank_text)

with open('preplexity.txt', 'w') as preplexity_file:
    preplexity_text = "\n".join(str(preplexity) for preplexity in preplexity_rank)
    preplexity_file.write(preplexity_text)

print "Find 'inlinks_count.txt', 'pagerank.txt' and 'preplexity.txt' under '{0}' directory\nCompleted in {1}".format(args.output_dir, datetime.now() - startTime)
