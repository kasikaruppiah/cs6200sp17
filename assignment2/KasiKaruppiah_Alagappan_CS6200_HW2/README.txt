1) The page rank algorithm is implemented in python and can be used with the following function

2) Use "python page_rank.py --help" to get the list of options to the script
kasi@kasi-Inspiron-N5010 /media/kasi/Studies/CS 6200/cs6200sp17/assignment2 $ python page_rank.py --help
usage: page_rank.py [-h] -i INLINKS_FILE [-o OUTPUT_DIR] [-v]

This is a page rank script created for cs6200sp17, assignment2

optional arguments:
  -h, --help            show this help message and exit
  -i INLINKS_FILE, --inlinks-file INLINKS_FILE
                        In-Link relationship file containing Graph
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory for the page rank output file
  -v, --verbose         Increase output verbosity

3) Sample implementation of the script
kasi@kasi-Inspiron-N5010 /media/kasi/Studies/CS 6200/cs6200sp17/assignment2 $ python page_rank.py -i ../Task1/inlinks.txt
Total Pages : 1000
Pages with no out-links : 0
Created '20170301062750' directory to save page rank results
Find 'inlinks_count.txt', 'pagerank.txt' and 'preplexity.txt' under '20170301062750' directory
Completed in 0:00:00.509536

kasi@kasi-Inspiron-N5010 /media/kasi/Studies/CS 6200/cs6200sp17/assignment2 $ python page_rank.py -i wt2g_inlinks
Total Pages : 183811
Pages with no out-links : 66175
Created '20170301062816' directory to save page rank results
Find 'inlinks_count.txt', 'pagerank.txt' and 'preplexity.txt' under '20170301062816' directory
Completed in 0:00:55.925585

kasi@kasi-Inspiron-N5010 /media/kasi/Studies/CS 6200/cs6200sp17/assignment2 $ python page_rank.py -i sample_inlinks
Total Pages : 6
Pages with no out-links : 0
Created '20170301063705' directory to save page rank results
Find 'inlinks_count.txt', 'pagerank.txt' and 'preplexity.txt' under '20170301063705' directory
Completed in 0:00:00.001797