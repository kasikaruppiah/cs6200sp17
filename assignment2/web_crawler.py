#!/usr/bin/python

import argparse
from datetime import datetime
import logging
import os
import errno
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
import re
import time
from collections import OrderedDict

startTime = datetime.now()

parser = argparse.ArgumentParser(description = 'This is a web crawler script created for cs6200sp17, assignment1')
parser.add_argument('-s', '--seed-url', help = 'Starting URL for the crawler', required = True)
parser.add_argument('-k', '--keyword', default = '', help = 'Keyword for focused crawling', required = False)
parser.add_argument('-l', '--limit', type = int, default = 1000, help = 'Maximum number of pages to be crawled', required = False)
parser.add_argument('-d', '--depth', type = int, default = 5, help = 'Level to be crawled')
parser.add_argument('-w', '--wait-between', type = int, default = 1, help = 'Seconds to wait between HTTP request', required = False)
parser.add_argument('-o', '--output-dir', default = datetime.now().strftime('%Y%m%d%H%M%S'), help = 'Output directory for the downloaded web pages and links text', required = False)
parser.add_argument('-a', '--alternate-crawling', action = 'store_true', help = 'Use Depth first search for crawling')
parser.add_argument('-v', '--verbose', action = 'store_true', help = 'Increase output verbosity')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format = '%(levelname)s : %(funcName)s - %(message)s', level = logging.DEBUG)
else:
    logging.basicConfig(format = '%(levelname)s : %(funcName)s - %(message)s')

def crawl():
    url_list = []
    inlinks = {}

    html_file_name_regex = re.compile('^https:\/\/en\.wikipedia\.org\/wiki\/(.*)')
    url = args.seed_url.rstrip('/')

    url_list.append({
        'Url' : url,
        'Level' : 1,
        'ParentDocumentID' : 'D0',
        'DocumentID' : html_file_name_regex.search(url).group(1),
    })
    url_crawled = []

    while url_list and len(url_crawled) < args.limit:
        url_dictionary = url_list.pop(0)
        url = url_dictionary['Url'].rstrip('/')

        if url not in url_crawled:
            if url_dictionary['ParentDocumentID'] == 'D0':
                inlinks[url_dictionary['DocumentID']] = []
            else:
                inlinks[url_dictionary['DocumentID']] = [url_dictionary['ParentDocumentID']]

            web_page, child_url_list = crawl_web_page(url)
            url_crawled.append(url)

            if url_dictionary['Level'] < args.depth and child_url_list:
                child_url_dict_list = []
                for link in child_url_list:
                    child_url_dict_list.append({
                        'Url' : link.rstrip('/'),
                        'Level' : url_dictionary['Level'] + 1,
                        'ParentDocumentID' : url_dictionary['DocumentID'],
                        'DocumentID' : html_file_name_regex.search(link).group(1),
                    })
                if args.alternate_crawling:
                    url_list = child_url_dict_list + url_list
                else:
                    url_list += child_url_dict_list

            time.sleep(args.wait_between)
        else:
            inlinks[url_dictionary['DocumentID']].append(url_dictionary['ParentDocumentID'])
    print "Crawled {0} links".format(len(url_crawled))

    while (url_list):
        url_dictionary = url_list.pop(0)
        if url_dictionary['DocumentID'] in inlinks and url_dictionary['ParentDocumentID'] in inlinks:
            inlinks[url_dictionary['DocumentID']].append(url_dictionary['ParentDocumentID'])

    try:
        os.mkdir(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
        pass
    os.chdir(args.output_dir)
    print "Created '{0}' directory to save crawl results".format(args.output_dir)

    with open('links.txt', 'w') as link_file:
        for url in (url_crawled):
            link_file.write("{0}\n".format(url.encode('utf-8')))
    with open('inlinks.txt', 'w') as inlink_file:
        for docid in inlinks:
            inlink_file.write("{0} {1}\n".format(docid, " ".join(inlinks[docid])))

def crawl_web_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    url_list = []
    href_regex = re.compile('^https:\/\/en\.wikipedia\.org\/wiki')
    keyword_regex = re.compile(re.escape(args.keyword), flags = re.IGNORECASE)

    for link in soup.find_all('a', href = re.compile('^[^#]((?!\/(Talk|User|User talk|Wikipedia|Wikipedia talk|File|File talk|MediaWiki|MediaWiki talk|Template|Template talk|Help|Help talk|Category|Category talk|Portal|Portal talk|Book|Book talk|Draft|Draft talk|Education Program|Education Program talk|TimedText|TimedText talk|Module|Module talk|Gadget|Gadget talk|Gadget definition|Gadget definition talk|Special|Media):).)+$'), string = True):
        child_url = urljoin(url, link.get('href'))
        if href_regex.match(child_url) and ((args.keyword and (keyword_regex.match(child_url) or keyword_regex.match(link.string))) or not args.keyword):
            url_list.append(child_url.split('#', 1)[0])

    return soup.prettify(), (list(OrderedDict.fromkeys(url_list)))

crawl()

print "Find 'links.txt' and 'inlinks.txt' under '{0}' directory\nCompleted in {1}".format(args.output_dir, datetime.now() - startTime)
