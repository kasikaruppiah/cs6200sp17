import cPickle
import os
import pprint
import sys

import numpy
from scipy import stats


def main(args):
    perfermance_summary = cPickle.load(
        open(
            os.path.join(args['BASE_DIRECTORY'], 'performance_summary.pkl'),
            'rb'))
    search_types_lst = []

    # take first element of perfermance_summary and save all search_type s in search_types_lst
    # for search_type in perfermance_summary.itervalues().next().iterkeys():
    for query_num in perfermance_summary:
        for search_type in perfermance_summary[query_num]:
            search_types_lst += [search_type]
        break

    significance_table = {}
    '''
    {
        'tfidf' = [0.12, 0.05, 0.21, 0.15, 0.33, ...]
        'bm25' = [0.11, 0.15, 0.12, 0.23, 0.31, ...]
        .
        .
        .
    }
    '''

    # this for loop will do this:
    # significance_table = {}  =>   significance_table = {'tfidf'=[], 'bm25'=[], ...}
    for search_type in search_types_lst:
        significance_table[search_type] = []

    # this for loop populates the significance_table
    for query_num in perfermance_summary:
        value_dict = perfermance_summary[query_num]
        # fill the i th value for each array in significance_table
        for search_type in search_types_lst:
            # length is the length of first list . for e.g., len(list for 'tfidf')
            length = len(significance_table.itervalues().next())
            significance_table[search_type].insert \
                (length,  value_dict[search_type])

    pval_table = []

    # total search engine runs. t-test will be run between every pair of these
    total_runs = len(significance_table)

    search_types_lst.sort()
    # don't delete the following line. Its for debugging
    file_ttest_result = open(
        os.path.join(args['BASE_DIRECTORY'], 'performance_T-test_result.txt'),
        'wb')
    file_ttest_result.write('Search A'.ljust(10) + ' - ' + 'Search B'.ljust(10)
                           + ' : ' + 'pval' + '\n')

    for x in xrange(0, total_runs - 1):
        search_A = search_types_lst[x]
        eff_score_A = significance_table[
            search_A]  # List of effectiveness scores of search A.
        temp_list = []

        for y in xrange(x + 1, total_runs):
            search_B = search_types_lst[y]
            eff_score_B = significance_table[
                search_B]  # List of effectiveness scores of search B.
            result = stats.ttest_ind(eff_score_A, eff_score_B)
            ttest_val = numpy.abs(result[0])
            n = len(significance_table.itervalues().next())
            pval = stats.t.sf(ttest_val, n - 1)
            # don't delete the following line. Its for debugging
            file_ttest_result.write(
                search_A.ljust(10) + ' - ' + search_B.ljust(10) + ' : ' + str(
                    pval) + '\n')
            temp_list += [pval]
        pval_table.append(temp_list)
    # don't delete the following line. Its for debugging
    file_ttest_result.write ('\n\nThe Null-Hypothesis is rejected if the p-value is less than alpha, '+\
    'which is \ntypically 0.05 for T-tests. Thus, if pval< 0.05, the results from the 2 searches is\
    significantly different and one of the algorithms is significantly better than the other.')
    file_ttest_result.close()

    print search_types_lst
    for array in pval_table:
        print(array)
    print "\tSaved t-test results in {} directory".format(
        args['BASE_DIRECTORY'])


if __name__ == '__main__':
    base_directory = raw_input("Enter full path of the base directory:")
    if os.path.isdir(base_directory):
        main({'BASE_DIRECTORY': base_directory})
    else:
        raise Exception(
            "can't open '{}': No such directory".format(token_directory))
