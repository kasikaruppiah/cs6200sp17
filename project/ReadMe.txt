a) The code for the project is present under the project folder.
b) The code can be build and compiled using PyCharm.
c) The following packages have to be imported for the program to build successfully.
	1) PyQt4
	2) nltk
	3) scipy
	4) beautifulSoup
	5) numpy
d) The search engine has an UI which can be triggered from the Start_Dialog.py.
e) The UI will ask for a Query. One query from the list of queries given should be entered and it gives 
   the top 10 documents for that query using BM25 retrieval model.
f) The extra points question task 2 can be tested using the tests mentioned above.


Output files:

1) Task 1 three baseline runs are are present inside the "output\Task 1" folder with the following names:

BM25_baseline  -> for BM25 retrieval model
Lucene_baseline -> for Lucene retrieval model
tf-idf_baseline  -> for tf-idf retrieval model

2) Task 2 two baseline runs are are present inside the "output\Task 2" folder with the following names:

BM25_Thesaurus_query_expansion  -> BM25 retrieval model used with Thesaurus Query expansion technique
tf-idf_Thesaurus_query_expansion  -> TFIDF retrieval model used with Thesaurus Query expansion technique

3) Task 3 four baseline runs are are present inside the "output\Task 3" folder with the following names:

BM25_stemming  -->  BM25 retrieval model used with stemming applied
BM25_stopping  --> BM25 retrieval model used with stopping applied
tf-idf_stemming  --> TFIDF retrieval model used with stemming applied
tf-idf_stopping  --> TFIDF retrieval model used with stopping applied

4) Phase 2 : Evaluation



5)  Extra points:

Task1:

1) test.py has the code to perform statistical analysis.
2) You can run it using python test.py file.
3) The analysis of this is present under in the file located at
    "output\Extra credit\Statistical_Test_Task1"
4) The output from test.py file is in output\Extra credit\Statistical_Test_Task1

Task2:

1) The search engine has an UI which can be triggered from the Start_Dialog.py.
2) The UI will ask for a Query. One query from the list of queries given should be entered and it gives 
   the top 10 documents with snippets and query highlighting for that query using BM25 retrieval model.
3) The snippets for each query for all the runs can checked in the .HTML files in the 
	"output\Extra credit\snippet generation_Task2" folder.


6) Individual python programs can be run from the command line using the following commands:

Createad Inverted Index

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -i
Enter full path of the raw html directory:project_files/cacm
Triggering inverted_index.
	Created 'project_files/corpus' directory to save tokens.
	Completed generating corpus from the raw html.
	Completed generating inverted index for the corpus.
	Created term document frequency and term frequency text in project_files for the inverted_index.
	Saved the dict as pickle files in project_files directory
Completed in 0:00:11.048955 seconds.


BaseLine Runs

BM25 retrieval model

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -b
Enter full path of the base directory:project_files
Enter full path of the query file:project_files/cacm.query.txt
Enter a keyword for file naming (Optional, Blank if not required):base
Enter full path of the relevance file:project_files/cacm.rel
	Completed loading inverted index from pickle files.
		Processed query 1
		Processed query 2
		Processed query 3
		Processed query 4
		Processed query 5
		Processed query 6
		Processed query 7
		Processed query 8
		Processed query 9
		Processed query 10
		Processed query 11
		Processed query 12
		Processed query 13
		Processed query 14
		Processed query 15
		Processed query 16
		Processed query 17
		Processed query 18
		Processed query 19
		Processed query 20
		Processed query 21
		Processed query 22
		Processed query 23
		Processed query 24
		Processed query 25
		Processed query 26
		Processed query 27
		Processed query 28
		Processed query 29
		Processed query 30
		Processed query 31
		Processed query 32
		Processed query 33
		Processed query 34
		Processed query 35
		Processed query 36
		Processed query 37
		Processed query 38
		Processed query 39
		Processed query 40
		Processed query 41
		Processed query 42
		Processed query 43
		Processed query 44
		Processed query 45
		Processed query 46
		Processed query 47
		Processed query 48
		Processed query 49
		Processed query 50
		Processed query 51
		Processed query 52
		Processed query 53
		Processed query 54
		Processed query 55
		Processed query 56
		Processed query 57
		Processed query 58
		Processed query 59
		Processed query 60
		Processed query 61
		Processed query 62
		Processed query 63
		Processed query 64
	Saved query results in project_files directory
Completed in 0:00:29.843479 seconds.

tf-idf retrieval model

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -t
Enter full path of the base directory:project_files
Enter full path of the query file:project_files/cacm.query.txt
Enter a keyword for file naming (Optional, Blank if not required):base
	Completed loading inverted index from pickle files.
		Processed query 1
		Processed query 2
		Processed query 3
		Processed query 4
		Processed query 5
		Processed query 6
		Processed query 7
		Processed query 8
		Processed query 9
		Processed query 10
		Processed query 11
		Processed query 12
		Processed query 13
		Processed query 14
		Processed query 15
		Processed query 16
		Processed query 17
		Processed query 18
		Processed query 19
		Processed query 20
		Processed query 21
		Processed query 22
		Processed query 23
		Processed query 24
		Processed query 25
		Processed query 26
		Processed query 27
		Processed query 28
		Processed query 29
		Processed query 30
		Processed query 31
		Processed query 32
		Processed query 33
		Processed query 34
		Processed query 35
		Processed query 36
		Processed query 37
		Processed query 38
		Processed query 39
		Processed query 40
		Processed query 41
		Processed query 42
		Processed query 43
		Processed query 44
		Processed query 45
		Processed query 46
		Processed query 47
		Processed query 48
		Processed query 49
		Processed query 50
		Processed query 51
		Processed query 52
		Processed query 53
		Processed query 54
		Processed query 55
		Processed query 56
		Processed query 57
		Processed query 58
		Processed query 59
		Processed query 60
		Processed query 61
		Processed query 62
		Processed query 63
		Processed query 64
	Saved query results in project_files directory
Completed in 0:00:16.981011 seconds.

Lucene retrieval model

Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\temp\index)
/mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project/project_files/index
Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\Users\mydir\docs)
[Acceptable file types: .xml, .html, .html, .txt]
/mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project/project_files/corpus

************************
3204 documents added.
************************
Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\Users\mydir\docs)
[Acceptable file types: .xml, .html, .html, .txt]
q
Enter the full path of the query file:
/mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project/project_files/cacm.query.txt
Processed query 44
Processed query 45
Processed query 46
Processed query 47
Processed query 48
Processed query 49
Processed query 50
Processed query 51
Processed query 52
Processed query 53
Processed query 10
Processed query 54
Processed query 11
Processed query 55
Processed query 12
Processed query 56
Processed query 13
Processed query 57
Processed query 14
Processed query 58
Processed query 15
Processed query 59
Processed query 16
Processed query 17
Processed query 18
Processed query 19
Processed query 1
Processed query 2
Processed query 3
Processed query 4
Processed query 5
Processed query 6
Processed query 7
Processed query 8
Processed query 9
Processed query 60
Processed query 61
Processed query 62
Processed query 63
Processed query 20
Processed query 64
Processed query 21
Processed query 22
Processed query 23
Processed query 24
Processed query 25
Processed query 26
Processed query 27
Processed query 28
Processed query 29
Processed query 30
Processed query 31
Processed query 32
Processed query 33
Processed query 34
Processed query 35
Processed query 36
Processed query 37
Processed query 38
Processed query 39
Processed query 40
Processed query 41
Processed query 42
Processed query 43
Completed processing queries from the file


Task 2


BM25 retrieval model - with query expansion

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -b -e
Enter full path of the base directory:project_files
Enter full path of the query file:project_files/cacm.query.txt
Enter a keyword for file naming (Optional, Blank if not required):thesaurus          
Enter full path of the relevance file:project_files/cacm.rel
	Completed loading inverted index from pickle files.
		Processed query 1
		Processed query 2
		Processed query 3
		Processed query 4
		Processed query 5
		Processed query 6
		Processed query 7
		Processed query 8
		Processed query 9
		Processed query 10
		Processed query 11
		Processed query 12
		Processed query 13
		Processed query 14
		Processed query 15
		Processed query 16
		Processed query 17
		Processed query 18
		Processed query 19
		Processed query 20
		Processed query 21
		Processed query 22
		Processed query 23
		Processed query 24
		Processed query 25
		Processed query 26
		Processed query 27
		Processed query 28
		Processed query 29
		Processed query 30
		Processed query 31
		Processed query 32
		Processed query 33
		Processed query 34
		Processed query 35
		Processed query 36
		Processed query 37
		Processed query 38
		Processed query 39
		Processed query 40
		Processed query 41
		Processed query 42
		Processed query 43
		Processed query 44
		Processed query 45
		Processed query 46
		Processed query 47
		Processed query 48
		Processed query 49
		Processed query 50
		Processed query 51
		Processed query 52
		Processed query 53
		Processed query 54
		Processed query 55
		Processed query 56
		Processed query 57
		Processed query 58
		Processed query 59
		Processed query 60
		Processed query 61
		Processed query 62
		Processed query 63
		Processed query 64
	Saved query results in project_files directory
Completed in 0:03:02.559104 seconds.

tf-idf retrieval model - with query expansion

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -t -e
Enter full path of the base directory:project_files
Enter full path of the query file:project_files/cacm.query.txt
Enter a keyword for file naming (Optional, Blank if not required):thesaurus
	Completed loading inverted index from pickle files.
		Processed query 1
		Processed query 2
		Processed query 3
		Processed query 4
		Processed query 5
		Processed query 6
		Processed query 7
		Processed query 8
		Processed query 9
		Processed query 10
		Processed query 11
		Processed query 12
		Processed query 13
		Processed query 14
		Processed query 15
		Processed query 16
		Processed query 17
		Processed query 18
		Processed query 19
		Processed query 20
		Processed query 21
		Processed query 22
		Processed query 23
		Processed query 24
		Processed query 25
		Processed query 26
		Processed query 27
		Processed query 28
		Processed query 29
		Processed query 30
		Processed query 31
		Processed query 32
		Processed query 33
		Processed query 34
		Processed query 35
		Processed query 36
		Processed query 37
		Processed query 38
		Processed query 39
		Processed query 40
		Processed query 41
		Processed query 42
		Processed query 43
		Processed query 44
		Processed query 45
		Processed query 46
		Processed query 47
		Processed query 48
		Processed query 49
		Processed query 50
		Processed query 51
		Processed query 52
		Processed query 53
		Processed query 54
		Processed query 55
		Processed query 56
		Processed query 57
		Processed query 58
		Processed query 59
		Processed query 60
		Processed query 61
		Processed query 62
		Processed query 63
		Processed query 64
	Saved query results in project_files directory
Completed in 0:00:29.741869 seconds.


Task 3


Stopping


Createad Inverted Index - with stopping

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -i -s
Enter full path of the raw html directory:project_files/cacm
Enter full path of the stop list file:project_files/common_words
Triggering inverted_index.
	Created 'project_files/corpus' directory to save tokens.
	Completed generating corpus from the raw html.
	Completed generating inverted index for the corpus.
	Created term document frequency and term frequency text in project_files for the inverted_index.
	Saved the dict as pickle files in project_files directory
Completed in 0:00:36.913188 seconds.

base search engine with stopping

BM25 retrieval model - with stopping

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -b
Enter full path of the base directory:project_files
Enter full path of the query file:project_files/cacm.query.txt
Enter a keyword for file naming (Optional, Blank if not required):stopping
Enter full path of the relevance file:project_files/cacm.rel
	Completed loading inverted index from pickle files.
		Processed query 1
		Processed query 2
		Processed query 3
		Processed query 4
		Processed query 5
		Processed query 6
		Processed query 7
		Processed query 8
		Processed query 9
		Processed query 10
		Processed query 11
		Processed query 12
		Processed query 13
		Processed query 14
		Processed query 15
		Processed query 16
		Processed query 17
		Processed query 18
		Processed query 19
		Processed query 20
		Processed query 21
		Processed query 22
		Processed query 23
		Processed query 24
		Processed query 25
		Processed query 26
		Processed query 27
		Processed query 28
		Processed query 29
		Processed query 30
		Processed query 31
		Processed query 32
		Processed query 33
		Processed query 34
		Processed query 35
		Processed query 36
		Processed query 37
		Processed query 38
		Processed query 39
		Processed query 40
		Processed query 41
		Processed query 42
		Processed query 43
		Processed query 44
		Processed query 45
		Processed query 46
		Processed query 47
		Processed query 48
		Processed query 49
		Processed query 50
		Processed query 51
		Processed query 52
		Processed query 53
		Processed query 54
		Processed query 55
		Processed query 56
		Processed query 57
		Processed query 58
		Processed query 59
		Processed query 60
		Processed query 61
		Processed query 62
		Processed query 63
		Processed query 64
	Saved query results in project_files directory
Completed in 0:02:02.526139 seconds.

tf-idf retrieval model - with stopping

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -t
Enter full path of the base directory:project_files
Enter full path of the query file:project_files/cacm.query.txt
Enter a keyword for file naming (Optional, Blank if not required):stopping
	Completed loading inverted index from pickle files.
		Processed query 1
		Processed query 2
		Processed query 3
		Processed query 4
		Processed query 5
		Processed query 6
		Processed query 7
		Processed query 8
		Processed query 9
		Processed query 10
		Processed query 11
		Processed query 12
		Processed query 13
		Processed query 14
		Processed query 15
		Processed query 16
		Processed query 17
		Processed query 18
		Processed query 19
		Processed query 20
		Processed query 21
		Processed query 22
		Processed query 23
		Processed query 24
		Processed query 25
		Processed query 26
		Processed query 27
		Processed query 28
		Processed query 29
		Processed query 30
		Processed query 31
		Processed query 32
		Processed query 33
		Processed query 34
		Processed query 35
		Processed query 36
		Processed query 37
		Processed query 38
		Processed query 39
		Processed query 40
		Processed query 41
		Processed query 42
		Processed query 43
		Processed query 44
		Processed query 45
		Processed query 46
		Processed query 47
		Processed query 48
		Processed query 49
		Processed query 50
		Processed query 51
		Processed query 52
		Processed query 53
		Processed query 54
		Processed query 55
		Processed query 56
		Processed query 57
		Processed query 58
		Processed query 59
		Processed query 60
		Processed query 61
		Processed query 62
		Processed query 63
		Processed query 64
	Saved query results in project_files directory
Completed in 0:00:26.597802 seconds.


Stemming

Create Inverted Index - with stemming

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -stem
Enter full path of the stem file:project_files/cacm_stem.txt
Triggering inverted_index.
	Created 'project_files/corpus' directory to save tokens.
	Completed generating corpus from the stem file.
	Completed generating inverted index for the corpus.
	Created term document frequency and term frequency text in project_files for the inverted_index.
	Saved the dict as pickle files in project_files directory
Completed in 0:00:23.795615 seconds.

base search engine with stopping

BM25 retrieval model - with stopping

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -b -stem-query
Enter full path of the base directory:project_files
Enter full path of the stem query file:project_files/cacm_stem.query.txt
Enter a keyword for file naming (Optional, Blank if not required):stemming
Enter full path of the relevance file:project_files/cacm.rel
	Completed loading inverted index from pickle files.
		Processed query 1
		Processed query 2
		Processed query 3
		Processed query 4
		Processed query 5
		Processed query 6
		Processed query 7
	Saved query results in project_files directory
Completed in 0:00:52.054871 seconds.

tf-idf retrieval model - with stopping

kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/trigger.py -t -stem-query
Enter full path of the base directory:project_files
Enter full path of the stem query file:project_files/cacm_stem.query.txt
Enter a keyword for file naming (Optional, Blank if not required):stemming
	Completed loading inverted index from pickle files.
		Processed query 1
		Processed query 2
		Processed query 3
		Processed query 4
		Processed query 5
		Processed query 6
		Processed query 7
	Saved query results in project_files directory
Completed in 0:00:19.782876 seconds.



kasi@kasi-Inspiron-N5010 /mnt/cfd8ee71-4ac1-4f36-ba13-f35edf4e4a2c/CS 6200/cs6200sp17_project $ python project/perfomance.py
Enter full path of the base directory:project_files
Enter full path of the relevance file:project_files/cacm.rel
	Saved perfomance results in project_files directory
