Task1 - HW4.java

The HW4.java requires the following jar files to work
	lucene-analyzers-common-4.7.2.jar
	lucene-core-4.7.2.jar
	lucene-queryparser-4.7.2.jar
Once the jar files have been implemeted compile and run the code.
The code prompts for index directory to save lucen index
	Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\temp\index)
Then enter the directory of the token files when prompted
	Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\Users\mydir\docs)
	[Acceptable file types: .xml, .html, .html, .txt]	
Once the files needed have been added hit "q" to start querying
When prompted enter the search query
	Enter the search query (q=quit):
The top 100 results would be displayed and a file with the same results would be created in the current directory
Once the querying is done hit "q" to exit

Task2 - bm25_ranking.py

Run the code by entering "python bm25_ranking.py"
The code promts for the token directory
	Enter full path of the token directory:
Once the index is created you're prompted for query strings
	Enter the search query (q=quit):
The top 100 query result are saved under the same directory