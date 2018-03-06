from __future__ import division

import cPickle
import glob
import os
from pprint import pprint

relevence_cacm = {}
'''
datastructure of relevence_cacm:
{
    1 : {'CACM1601': True, 'CACM1795': True, 'CACM1811': True,},
    2 : {'CACM2651': True},
    3 : {'CACM1198': True, 'CACM1338': True, 'CACM1877': True,},
    .
    .
    .
}
'''
# store average_precision of each query for t-test calculation
avg_precisions = {}
'''
{
    1 : {'bm25': 0.0136, 'tfidf' : 0.0191, ...},
    2 : {'bm25': 0.0181, 'tfidf' : 0.025, ...},
    .
    .
    .
}
'''


# args: RELEVANCE_FILELOCATION, BASE_DIRECTORY
def main(args):

    file_cacm_rel = open(args['RELEVANCE_FILELOCATION'])
    for line in file_cacm_rel:
        line_arr = line.split()
        query_num = line_arr[0]
        docids = line_arr[2].split("-")
        docids[1] = '{:04d}'.format(int(docids[1]))
        doc_name = ''.join(docids)
        # add to dictionary relevence_cacm
        if query_num in relevence_cacm:
            relevence_cacm[query_num][doc_name] = True
        else:
            relevence_cacm[query_num] = {doc_name: True}

    mean_avg_precisions = {}
    '''
    {
        'tfidf' : { 'sum': 152.424, 'rrank': 6.4446, 'count': 52},
        'bm25' : { 'sum': 162.96, 'rrank':  7.3405, 'count': 52},
        .
        .
        .
    }
    '''

    # a list of search_type 's to keep to write file_map_smry
    search_types_lst = []
    '''
    ['tfidf', 'bm25', ...]
    '''

    # a dict to store all
    #   1. Average precision for each query for each run
    #   2. Reciprocal rank for each query for each run
    #   3. P@K for K=5 for each query for each run
    #   4. P@K for K=20 for each query for each run
    all_avg_precisions = \
    {
        'avg_precisions' :{},
        'reciprocal_ranks' :{},
        'p_at_5' :{},
        'p_at_20' :{}
    }
    '''
    datastructure for all_avg_precisions
    {
        avg_precisions : {
                            1: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 1
                            2: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 2
                            .
                            .
                            52: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 53
                        } 
        reciprocal_ranks : {
                            1: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 1
                            2: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 2
                            .
                            .
                            52: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 53
                            } 
        p_at_5 : {
                    1: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 1
                    2: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 2
                    .
                    .
                    52: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 53
                } 
    p_at_20 : {
                    1: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 1
                    2: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 2
                    .
                    .
                    52: {'tfidf': 0.234, 'bm25': 0.234, ...}  //for query 53
                } 

    }
    '''

    list_files = glob.glob(
        os.path.join(args['BASE_DIRECTORY'], '*_query_*.txt'))
    for file_path in list_files:
        # get data from the filename:
        filename = os.path.splitext(os.path.basename(file_path))[0]
        arr_file_name = filename.split('_query_')
        search_type = arr_file_name[0]  # 'bm25' or 'tfidf' or ...
        if search_type[-4:] == 'stem':
            continue  # not checking performance for
        query_num = arr_file_name[1]  # '1' or '2' ... or '64'
        # add search_type to search_types_lst
        if search_type not in search_types_lst:
            search_types_lst += [search_type]
        # if relevance judgement not provided in relevence_cacm, skip.
        if query_num not in relevence_cacm:
            continue
        # open read-file and write-file:
        file_query_results = open(file_path, 'rb')
        file_measure = open(
            os.path.join(args['BASE_DIRECTORY'], filename + '.per'), 'wb')
        file_measure.write('Rank'.center(15) + 'Relevance'.center(25) +
                           'Precision'.center(25) + 'Recall'.center(25) + '\n')
        # variables for Relevance and Precision:
        total_relevant = len(relevence_cacm[query_num])
        relevant_docs_found = 0.0
        rank = 0.0
        sum_precisions = 0.0  # used as numerator for AP for MAR
        count = 0  # used as denominator for AP for MAR
        rank_1st_rel_doc = -1  # used to find reciprocal rank for MRR
        pk5 = 0.0  # for storing P@K , k=5
        pk20 = 0.0  # for storing P@K , k=20
        # looping through lines of query-results-file and writing precision file:
        for line in file_query_results:
            line_arr = line.split()
            if line_arr[0] == 'query_id':
                continue
            count += 1
            rank = int(line_arr[3])
            doc_name = line_arr[2]
            relevance = "N"
            if doc_name in relevence_cacm[query_num]:
                relevance = "R"
                relevant_docs_found += 1
                # if this is the 1st relevant doc of this query, store it.:
                if rank_1st_rel_doc == -1:
                    rank_1st_rel_doc = rank
            precision = relevant_docs_found / rank
            # precision_string = str(relevant_docs_found) + '/' + str(rank) + '=' # for debugging
            recall = relevant_docs_found / total_relevant
            # recall_string = str(relevant_docs_found) + '/' + str(total_relevant) + '=' # for debugging
            # uncomment the following line for debugging
            # print 'rank = ', rank, ', precision=', precision_string, precision,\
            #     'recall=', recall_string, recall
            if rank == 5:
                pk5 = precision
            elif rank == 20:
                pk20 = precision
            file_measure.write(
                str(rank).center(15) + relevance.center(25) + str(precision)
                .center(25) + str(recall).center(25) + "\n")
            sum_precisions += precision
        if rank_1st_rel_doc == -1:
            reciprocal_rank = 0
        else:
            reciprocal_rank = 1.0 / rank_1st_rel_doc
        file_measure.write('\n\nReciprocal Rank: ' + str(reciprocal_rank))
        # file_measure.write('\n sum_precisions: '+str(sum_precisions)+', count:'+ str(count)) # for debugging
        average_precision = sum_precisions / count
        file_measure.write('\nAverage Precision: ' + str(average_precision))
        file_measure.write('\nP@K, K = 5 and 20: ')
        file_measure.write('\n\tP@K for K =  5: ' + str(pk5))
        file_measure.write('\n\tP@K for K = 20: ' + str(pk20))
        file_query_results.close()
        file_measure.close()
        # write the data in all_avg_precisions to compare different precions
        all_avg_precisions['avg_precisions'][query_num] = average_precision
        all_avg_precisions['reciprocal_ranks'][query_num] = reciprocal_rank
        all_avg_precisions['p_at_5'][query_num] = pk5
        all_avg_precisions['p_at_20'][query_num] = pk20


        # add average_precision to avg_precisions for t-test calculation
        if query_num in avg_precisions:
            avg_precisions[query_num][search_type] = average_precision
        else:
            avg_precisions[query_num] = {search_type: average_precision}

        # add the mean_avg_precisions & reciprocal_rank to sum_precisions:
        if search_type in mean_avg_precisions:
            mean_avg_precisions[search_type]['sum'] += average_precision
            mean_avg_precisions[search_type]['rrank'] += reciprocal_rank
            mean_avg_precisions[search_type]['count'] += 1
        else:
            mean_avg_precisions[search_type] = {
                'sum': average_precision,
                'rrank': reciprocal_rank,
                'count': 1
            }
    # print all_avg_precisions

    # write MAP and MRR in a file:
    file_map_mrr = open(
        os.path.join(args['BASE_DIRECTORY'], 'performance_measure.txt'), 'wb')
    for search_type in mean_avg_precisions:
        file_map_mrr.write(search_type + ':\n')
        this_search = mean_avg_precisions[search_type]
        mean_ap = this_search['sum'] / this_search['count']
        file_map_mrr.write('\tMean Average Precision: ' + str(mean_ap) + '\n')
        mrr = this_search['rrank'] / this_search['count']
        file_map_mrr.write('\tMean Reciprocal Rank: ' + str(mrr) + '\n')
    file_map_mrr.close()

    # write avg_precisions in a file that will be read when t-test is run
    file_map_smry = open(
        os.path.join(args['BASE_DIRECTORY'], 'performance_summary.txt'), 'wb')
    file_map_smry.write('query'.ljust(10))
    for search_type in search_types_lst:
        file_map_smry.write(search_type.center(20))
    file_map_smry.write('\n')
    for query_num in avg_precisions:
        this_dict = avg_precisions[query_num]
        file_map_smry.write(str(query_num).center(10))
        for search_type in search_types_lst:
            if search_type in this_dict:
                value = this_dict[search_type]
            else:
                value = '?'
            file_map_smry.write(str(value).center(20))
        file_map_smry.write('\n')
    file_map_smry.close()

    # save the avg_precisions using pickle. It will be used for t-test of Bonus task
    cPickle.dump(avg_precisions,
                 open(
                     os.path.join(args['BASE_DIRECTORY'],
                                  'performance_summary.pkl'), 'wb'))
    print "\tSaved perfomance results in {} directory".format(
        args['BASE_DIRECTORY'])


if __name__ == '__main__':
    base_directory = raw_input("Enter full path of the base directory:")
    if os.path.isdir(base_directory):
        relevance_file_location = raw_input(
            "Enter full path of the relevance file:")
        if not os.path.isfile(relevance_file_location):
            raise Exception("can't open '{}': No such directory".format(
                relevance_file_location))
        main({
            'RELEVANCE_FILELOCATION': relevance_file_location,
            'BASE_DIRECTORY': base_directory
        })
    else:
        raise Exception(
            "can't open '{}': No such directory".format(base_directory))
