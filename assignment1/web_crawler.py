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

try:
    os.mkdir(args.output_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise e
    pass
os.chdir(args.output_dir)
print "Created '{0}' directory to save crawl results".format(args.output_dir)

def crawl():
    url_list = []
    url_list.append({
        'Url' : args.seed_url,
        'Level' : 1,
    })
    url_crawled = []

    while (url_list and len(url_crawled) < args.limit):
        url_dictionary = url_list.pop(0)
        url = url_dictionary['Url'].rstrip('/')
        html_file_name = re.compile('.*\/(.*)').search(url).group(1)

        if url not in url_crawled:
            web_page, child_url_list = crawl_web_page(url)

            with open(html_file_name, 'w') as html_file:
                html_file.write(web_page.encode('utf-8'))

            url_crawled.append(url)

            if url_dictionary['Level'] < args.depth and child_url_list:
                child_url_dict_list = []
                for link in child_url_list:
                    child_url_dict_list.append({
                        'Url' : link,
                        'Level' : url_dictionary['Level'] + 1,
                    })
                if args.alternate_crawling:
                    url_list = child_url_dict_list + url_list
                else:
                    url_list += child_url_dict_list

            time.sleep(args.wait_between)

    with open('links.txt', 'w') as link_file:
        for url in (url_crawled):
            link_file.write("{0}\n".format(url.encode('utf-8')))
    print "Crawled {0} links".format(len(url_crawled))

def crawl_web_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    url_list = []
    href_regex = re.compile('^https:\/\/en\.wikipedia\.org\/wiki')
    keyword_regex = re.compile(re.escape(args.keyword), flags = re.IGNORECASE)

    for contentdiv in soup.find_all('div', {'id' : 'content'}):
        for link in soup.find_all('a', href = re.compile('^[^#]((?!\/(Talk|User|User talk|Wikipedia|Wikipedia talk|File|File talk|MediaWiki|MediaWiki talk|Template|Template talk|Help|Help talk|Category|Category talk|Portal|Portal talk|Book|Book talk|Draft|Draft talk|Education Program|Education Program talk|TimedText|TimedText talk|Module|Module talk|Gadget|Gadget talk|Gadget definition|Gadget definition talk|Special|Media):).)+$'), string = True):
            child_url = urljoin(url, link.get('href'))
            if href_regex.match(child_url) and ((args.keyword and (keyword_regex.match(child_url) or keyword_regex.match(link.string))) or not args.keyword):
                url_list.append(child_url.split('#', 1)[0])

    return soup.prettify(), url_list

crawl()

print "Find the links crawled in 'links.txt' under '{0}' directory\nCompleted in {1}".format(args.output_dir, datetime.now() - startTime)
