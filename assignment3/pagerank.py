#!/usr/bin/python

# Link Analysis and PageRank Implementation

import math
import os
from collections import OrderedDict

DAMPING_FACTOR = 0.85


# args: BASE_DIRECTORY, IN_LINK_FILE, CONVERGENCE, ITERATIONS
def generate_pagerank(args):
    in_link = __create_in_link__({
        'BASE_DIRECTORY': args['BASE_DIRECTORY'],
        'IN_LINK_FILE': args['IN_LINK_FILE']
    })
    total_documents = len(in_link)
    out_link = __create_out_link__({'IN_LINK': in_link})
    out_link_count = __get_out_link_count__({'OUT_LINK': out_link})
    sink_nodes = __get_sink_nodes__({'IN_LINK': in_link, 'OUT_LINK': out_link})

    pagerank = {}
    for documentid in in_link:
        pagerank[documentid] = 1.0 / total_documents
    perplexities = [__calculate_perplexity__({'PAGERANK': pagerank})]
    index = 0

    while index < args['ITERATIONS']:
        new_pagerank = {}
        sink_pagerank = 0
        for documentid in sink_nodes:
            sink_pagerank += pagerank[documentid]
        for documentid in in_link:
            new_pagerank[documentid] = (1 - DAMPING_FACTOR) / total_documents
            new_pagerank[
                documentid] += DAMPING_FACTOR * sink_pagerank / total_documents
            for in_link_documentid in in_link[documentid]:
                new_pagerank[documentid] += DAMPING_FACTOR * pagerank[
                    in_link_documentid] / out_link_count[in_link_documentid]
        for documentid in in_link:
            pagerank[documentid] = new_pagerank[documentid]
        new_perplexity = __calculate_perplexity__({'PAGERANK': pagerank})
        if abs(new_perplexity - perplexities[-1]) < args['CONVERGENCE']:
            index += 1
        else:
            index = 0
        perplexities.append(new_perplexity)
    print "\tCompleted generating pagerank for the in-link relationship."

    with open(os.path.join(args['BASE_DIRECTORY'], 'perplexity.txt'),
              'w') as perplexity_file:
        perplexity_text = "\n".join(
            str(perplexity) for perplexity in perplexities)
        perplexity_file.write(perplexity_text)
    print "\tCreated 'perplexity.txt' in {} with list of all perplexities.".format(
        args['BASE_DIRECTORY'])
    with open(os.path.join(args['BASE_DIRECTORY'], 'pagerank.txt'),
              'w') as pagerank_file:
        pagerank_text = ''
        for key in sorted(pagerank, key=pagerank.get, reverse=True):
            pagerank_text += "{0}\t:\t{1}\n".format(key, pagerank[key])
        pagerank_file.write(pagerank_text)
    print "\tCreated 'pagerank.txt' in {} with list ordered pagerank for in-link relationship.".format(
        args['BASE_DIRECTORY'])


# args: BASE_DIRECTORY, IN_LINK_FILE
def __create_in_link__(args):
    in_link = {}
    with open(os.path.join(args['BASE_DIRECTORY'], args['IN_LINK_FILE']),
              'r') as in_link_file:
        for line in in_link_file:
            documentids = (list(OrderedDict.fromkeys(line.strip().split(' '))))
            in_link_documentid = documentids.pop(0)
            in_link[in_link_documentid] = documentids
    return in_link


# args: IN_LINK
def __create_out_link__(args):
    out_link = {}
    for in_link_documentid in args['IN_LINK']:
        for in_link in args['IN_LINK'][in_link_documentid]:
            if in_link in out_link:
                out_link[in_link].append(in_link_documentid)
            else:
                out_link[in_link] = [in_link_documentid]
    return out_link


# args: OUT_LINK
def __get_out_link_count__(args):
    out_link_count = {}
    for documentid in args['OUT_LINK']:
        out_link_count[documentid] = len(args['OUT_LINK'][documentid])
    return out_link_count


# args: IN_LINK, OUT_LINK
def __get_sink_nodes__(args):
    sink_nodes = []
    for in_link_documentid in args['IN_LINK']:
        if in_link_documentid not in args['OUT_LINK']:
            sink_nodes.append(in_link_documentid)
    return sink_nodes


# args: PAGERANK
def __calculate_perplexity__(args):
    shannon_entropy = 0
    for documentid in args['PAGERANK']:
        shannon_entropy += args['PAGERANK'][documentid] * math.log(
            args['PAGERANK'][documentid], 2)
    return pow(2, -shannon_entropy)
