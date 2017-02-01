#!/usr/bin/python

import argparse
import logging
import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
import re
#import sys
import time

parser = argparse.ArgumentParser(description = 'This is a web crawler script created for cs6200sp17, assignment1')
parser.add_argument('-s', '--seed-url', help = 'Starting URL for the crawler', required = True)
parser.add_argument('-l', '--limit', type = int, default = 1000, help = 'Maximum number of pages to be crawled', required = False)
parser.add_argument('-w', '--wait-between', type = int, default = 1, help = 'Seconds to wait between HTTP request', required = False)
parser.add_argument('-v', '--verbose', action = 'store_true', help = 'Increase output verbosity')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format = '%(levelname)s : %(funcName)s - %(message)s', level = logging.DEBUG)
else:
    logging.basicConfig(format = '%(levelname)s : %(funcName)s - %(message)s')

def crawl_web_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    logging.error('Update logic to filter noisy pages')
    url_list = []
    for link in soup.find_all('a', href = re.compile('^[^#][^?]+$')):
        url_list.append(urljoin(url, link.get('href')))
    return soup.prettify(), url_list

def crawl():
    pages_crawled = 0
    url_list = [args.seed_url]
    link_file = open('link.txt', 'w')
    while (url_list and pages_crawled < args.limit):
        url = url_list[0]
        web_page_regex = re.compile('.*\/(.*)')
        html_file_name = web_page_regex.search(url).group(1)
        web_page, child_url_list = crawl_web_page(url)
        html_file = open(html_file_name, 'w')
        html_file.write(web_page.encode('utf-8'))
        html_file.close()
        url_list.pop(0)
        url_list += child_url_list
        pages_crawled += 1
        link_file.write(url + "\n")
        time.sleep(args.wait_between)
    link_file.close()

crawl()
