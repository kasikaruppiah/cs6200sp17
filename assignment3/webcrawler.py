#!/usr/bin/python

# Implementing your own web crawler. Performing focused crawling

import os
import re
import time
from urlparse import urljoin

import requests
from bs4 import BeautifulSoup

HTML_DIRECTORY = 'raw_html'

__urls_frontier__ = []  # List of URLs to be crawled
__urls_crawled__ = []  # List of URLs crawled


# args: BASE_DIRECTORY, SEED_URL, KEYWORD, LIMIT, DEPTH, DEPTH_FIRST_CRAWL,
#       POLITENESS
def crawl(args):
    global __urls_frontier__
    html_filename_regex = re.compile('^(.*)\/(.*)$')
    keyword_regex = re.compile('^.*$')
    if 'KEYWORD' in args:
        keyword_regex = re.compile(
            '^.*{}.*$'.format(args['KEYWORD']), flags=re.IGNORECASE)
    base_url = html_filename_regex.search(args['SEED_URL']).group(1)
    __urls_frontier__.append({'DEPTH': 1, 'URL': args['SEED_URL']})

    while len(__urls_crawled__) < args['LIMIT'] and __urls_frontier__:
        url_dict = __urls_frontier__.pop(0)
        if (url_dict['URL'] not in __urls_crawled__):
            __crawl_url__({
                'BASE_URL':
                re.compile('^{}.*$'.format(base_url)),
                'DEPTH':
                args['DEPTH'],
                'DEPTH_FIRST_CRAWL':
                args['DEPTH_FIRST_CRAWL'],
                'HTML_FILENAME_REGEX':
                html_filename_regex,
                'KEYWORD':
                args.get('KEYWORD', None),
                'KEYWORD_REGEX':
                keyword_regex,
                'RAW_HTML_DIRECTORY':
                os.path.join(args['BASE_DIRECTORY'], HTML_DIRECTORY),
                'URL_DICT':
                url_dict
            })
        time.sleep(args['POLITENESS'])
    with open(os.path.join(args['BASE_DIRECTORY'], 'urls_crawled.txt'),
              'w') as urls_crawled_file:
        urls_crawled_file.write("\n".join(__urls_crawled__))


# args: URL_DICT, HTML_FILENAME_REGEX, RAW_HTML_DIRECTORY, DEPTH, KEYWORD,
#       KEYWORD_REGEX, DEPTH_FIRST_CRAWL
def __crawl_url__(args):
    global __urls_frontier__, __urls_crawled__

    request_object = requests.get(args['URL_DICT']['URL'])
    if request_object.url not in __urls_crawled__:
        html_file_name = args['HTML_FILENAME_REGEX'].search(
            args['URL_DICT']['URL']).group(2)
        html = request_object.text
        with open(
                os.path.join(args['RAW_HTML_DIRECTORY'], html_file_name),
                'w') as html_file:
            html_file.write(html.encode('utf-8'))
        if args['URL_DICT']['DEPTH'] < args['DEPTH']:
            depth = args['URL_DICT']['DEPTH'] + 1
            child_urls_frontier = []
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find(
                    'div', id='content'
            ).find_all(
                    'a',
                    href=re.compile(
                        '^[^#]((?!\/(Talk|User|User talk|Wikipedia|Wikipedia talk|File|File talk|MediaWiki|MediaWiki talk|Template|Template talk|Help|Help talk|Category|Category talk|Portal|Portal talk|Book|Book talk|Draft|Draft talk|Education Program|Education Program talk|TimedText|TimedText talk|Module|Module talk|Gadget|Gadget talk|Gadget definition|Gadget definition talk|Special|Media):).)+$'
                    ),
                    string=True):
                child_url = urljoin(args['URL_DICT']['URL'],
                                    link.get('href')).split('#')[0]
                if args['BASE_URL'].match(child_url) and (
                    (args['KEYWORD'] and
                     (args['KEYWORD_REGEX'].match(child_url) or
                      args['KEYWORD_REGEX'].match(link.string))) or
                        not args['KEYWORD']):
                    child_urls_frontier.append({
                        'DEPTH': depth,
                        'URL': child_url
                    })
            if args['DEPTH_FIRST_CRAWL']:
                __urls_frontier__ = child_urls_frontier + __urls_frontier__
            else:
                __urls_frontier__ += child_urls_frontier
        __urls_crawled__.append(args['URL_DICT']['URL'])
