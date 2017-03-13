#!/usr/bin/python

# Implementing your own inverted indexer. Text processing and corpus statistics.
import errno
import os
import re
import string

from bs4 import BeautifulSoup


# args: BASE_DIRECTORY, RAW_HTML_DIRECTORY, TOKEN_DIRECTORY
def make_corpus(args):
    source_directory = os.path.join(args['BASE_DIRECTORY'],
                                    args['RAW_HTML_DIRECTORY'])
    destination_directory = os.path.join(args['BASE_DIRECTORY'],
                                         args['TOKEN_DIRECTORY'])
    for filename in os.listdir(source_directory):
        tokenize_file(source_directory, filename, destination_directory)


def tokenize_file(source_directory, filename, destination_directory):
    # Get contents of file
    file_contents = open(os.path.join(source_directory, filename), 'r').read()

    # Pre-Process file contents, just the content of the wiki
    soup = BeautifulSoup(file_contents, 'html.parser').find(
        'div', id='content')

    # remove all script and style elements
    for html_tag in soup(["script", "style"]):
        html_tag.extract()
    # remove all html tags
    text = soup.get_text()
    # remove URL's
    text = re.sub(r"http\S+", " ", text)
    # case folding
    text = text.lower()
    # TODO: should em-dash be replaced with "-"
    # remove all non printable characters
    text = re.sub(r"[^\x00-\x7f]", " ", text)
    # remove all string punctuations other than "-", ".", ","
    text = re.sub(r"[!\"#$%&\'()*+/:;<=>?@[\\\]^_`{|}~]", " ", text)
    # remove all "-" not between text
    # TODO: improve efficiency - find alternative to |
    text = re.sub(r"(?<![a-zA-Z0-9])-|-(?![a-zA-Z0-9])", " ", text)
    # remove all ,", "." in text not between digits

    # remove multiple \s+ characters
    text = ' '.join(text.split())

    filename = filename.translate(None, "_-") + '.txt'
    open(os.path.join(destination_directory, filename),
         'w').write(text.encode('utf-8'))
