#!/usr/bin/python
from __future__ import division

import cPickle as pickle
import math
import os
import sys

__training_data__ = {}
__likelihood_probability__ = {}
__prior_probability__ = {}
__default_probability__ = {}


# args: TEST_DIRECTORY
def __classify_documents__(args):
    classification = {}
    doc_score = {}
    classes = __training_data__.keys()
    for C in classes:
        classification[C] = []
    for D in os.listdir(args['TEST_DIRECTORY']):
        doc_score[D] = {}
        for C in classes:
            doc_score[D][C] = __prior_probability__[C]
        words = open(os.path.join(args['TEST_DIRECTORY'], D),
                     'r').read().split()
        for word in words:
            for C in classes:
                if word in __likelihood_probability__[C]:
                    doc_score[D][C] += __likelihood_probability__[C][word]
                else:
                    doc_score[D][C] += __default_probability__[C]
        doc_class = max(doc_score[D], key=doc_score[D].get)
        doc_score[D]['CLASS'] = doc_class
        classification[doc_class].append(D)
    with open(sys.argv[3], 'w') as predictions_file:
        predictions_file.write("Filename\t\t" + "\t\t".join(classes) +
                               "\t\tClass\n")
        predictions_file.write("\n".join("\t\t".join(
            map(str, [D] + doc_score[D].values())) for D in doc_score))
    print "Document Classification:\nTest Directory: {}\n{}\t{}".format(
        args['TEST_DIRECTORY'], 'Class', 'Document')
    for C in classification:
        print "{}\t{}".format(C, len(classification[C]))


if len(sys.argv) == 4:
    model_file = sys.argv[1]
    if os.path.isfile(model_file):
        __training_data__, __likelihood_probability__, __prior_probability__, __default_probability__ = pickle.load(
            open(model_file, "rb"))
    else:
        raise Exception("can't open '{}': No such file".format(model_file))
    test_directory = sys.argv[2]
    if os.path.isdir(test_directory):
        __classify_documents__({'TEST_DIRECTORY': test_directory})
    else:
        raise Exception(
            "can't open '{}': No such directory".format(test_directory))
else:
    raise Exception(
        "Usage:\npython nbtest.py <model-file> <test-directory> <predictions-file>"
    )
