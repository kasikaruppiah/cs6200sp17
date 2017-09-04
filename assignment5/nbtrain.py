#!/usr/bin/python

from __future__ import division

import cPickle as pickle
import math
import os
import sys
from collections import Counter

__training_data__ = {}
__training_stats__ = {}
__likelihood_probability__ = {}
__prior_probability__ = {}
__default_probability__ = {}


# args: TRAINING_DIRECTORY
def __process_training_documents__(args):
    global __training_data__, __training_stats__
    V = set()
    __training_stats__['N'] = 0
    classes = next(os.walk(args['TRAINING_DIRECTORY']))[1]
    for C in classes:
        __training_data__[C] = {}
        __training_stats__[C] = 0
        for D in os.listdir(os.path.join(args['TRAINING_DIRECTORY'], C)):
            __training_stats__['N'] += 1
            __training_stats__[C] += 1
            words = open(os.path.join(args['TRAINING_DIRECTORY'], C, D),
                         'r').read().split()
            v = Counter(words)
            V = V.union(v.keys())
            for word, frequency in v.iteritems():
                if word not in __training_data__[C]:
                    __training_data__[C][word] = {}
                __training_data__[C][word][D] = frequency
    words_removed = []
    for word in V:
        word_count = 0
        for C in classes:
            word_count += sum(__training_data__[C].get(word, {}).values())
        if word_count < 5:
            for C in classes:
                __training_data__[C].pop(word, None)
            words_removed.append(word)
    V = V.difference(words_removed)
    __calculate_probability__({'VOCABULARY': V})


# args: VOCABULARY
def __calculate_probability__(args):
    global __likelihood_probability__, __prior_probability__, __default_probability__
    vocabulary_size = len(args['VOCABULARY'])
    for C in __training_data__.keys():
        __likelihood_probability__[C] = {}
        __prior_probability__[C] = math.log(__training_stats__[C] /
                                            __training_stats__['N'])
        class_frequency = 0
        for word in __training_data__[C]:
            class_frequency += sum(__training_data__[C][word].values())
        __default_probability__[C] = math.log(
            (1 + 0) / (class_frequency + vocabulary_size))
        for word in __training_data__[C]:
            term_frequency = sum(__training_data__[C][word].values())
            __likelihood_probability__[C][word] = math.log(
                (1 + term_frequency) / (class_frequency + vocabulary_size))
    '''
    pos_neg = {}
    neg_pos = {}
    for word in args['VOCABULARY']:
        word_pos = __likelihood_probability__['pos'].get(
            word, __default_probability__['pos'])
        word_neg = __likelihood_probability__['neg'].get(
            word, __default_probability__['neg'])
        pos_neg[word] = word_pos - word_neg
        neg_pos[word] = word_neg - word_pos
    for word in sorted(pos_neg, key=pos_neg.get, reverse=True)[:20]:
        print "{}\t\t{}".format(word, pos_neg[word])
    print "\n\n\n\n\n"
    for word in sorted(neg_pos, key=neg_pos.get, reverse=True)[:20]:
        print "{}\t\t{}".format(word, neg_pos[word])
    '''
    pickle.dump([
        __training_data__, __likelihood_probability__, __prior_probability__,
        __default_probability__
    ], open(sys.argv[2], 'wb'))


if len(sys.argv) == 3:
    training_directory = sys.argv[1]
    if os.path.isdir(training_directory):
        __process_training_documents__({
            'TRAINING_DIRECTORY': training_directory
        })
    else:
        raise Exception(
            "can't open '{}': No such directory".format(training_directory))
else:
    raise Exception(
        "Usage:\npython nbtrain.py <training-directory> <model-file>")
