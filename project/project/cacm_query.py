#!/usr/bin/python

from bs4 import BeautifulSoup


# args: FILELOCATION
def get_queries(args):
    queries = {}
    file_contents = open(args['FILELOCATION'], 'r').read()
    soup = BeautifulSoup(file_contents, 'lxml')
    for doc in soup.find_all('doc'):
        docno = doc.find('docno')
        queries[docno.get_text().strip()] = docno.next_sibling.strip()
    return queries
