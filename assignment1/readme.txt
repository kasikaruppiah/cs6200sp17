1) The crawler is written in Python and needs BeautifulSoup library. Instructions to setup BeautifulSoup can be found at

https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

2) Get to the directory where "web_crawler.py" is present. To view list of available options enter "python web_crawler.py -h"

kasi@kasi-Inspiron-N5010 /media/kasi/Studies/CS 6200/cs6200sp17/assignment1 $ python web_crawler.py -h
usage: web_crawler.py [-h] -s SEED_URL [-k KEYWORD] [-l LIMIT] [-d DEPTH]
                      [-w WAIT_BETWEEN] [-o OUTPUT_DIR] [-a] [-v]

This is a web crawler script created for cs6200sp17, assignment1

optional arguments:
  -h, --help            show this help message and exit
  -s SEED_URL, --seed-url SEED_URL
                        Starting URL for the crawler
  -k KEYWORD, --keyword KEYWORD
                        Keyword for focused crawling
  -l LIMIT, --limit LIMIT
                        Maximum number of pages to be crawled
  -d DEPTH, --depth DEPTH
                        Level to be crawled
  -w WAIT_BETWEEN, --wait-between WAIT_BETWEEN
                        Seconds to wait between HTTP request
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory for the downloaded web pages and
                        links text
  -a, --alternate-crawling
                        Use Depth first search for crawling
  -v, --verbose         Increase output verbosity

3) For Task 1 enter the command "python web_crawler.py -s 'https://en.wikipedia.org/wiki/Sustainable_energy' -o 'Task1'"

kasi@kasi-Inspiron-N5010 ~/Desktop $ python web_crawler.py -s "https://en.wikipedia.org/wiki/Sustainable_energy" -o 'Task1'
Created 'Task1' directory to save crawl results
Crawled 1000 links
Find the links crawled in 'links.txt' under 'Task1' directory
Completed in 0:28:59.577122

4) For Task 2A enter the command "python web_crawler.py -s 'https://en.wikipedia.org/wiki/Sustainable_energy' -k 'solar' -o 'Task2A'"

kasi@kasi-Inspiron-N5010 /media/kasi/Studies/CS 6200/cs6200sp17/assignment1 $ python web_crawler.py -s "https://en.wikipedia.org/wiki/Sustainable_energy" -k "solar" -o "Task2A"
Created 'Task2A' directory to save crawl results
Crawled 434 links
Find the links crawled in 'links.txt' under 'Task2A' directory
Completed in 0:11:28.587697

5) For Task 2B enter the command "python web_crawler.py -s 'https://en.wikipedia.org/wiki/Sustainable_energy' -k 'solar' -o 'Task2B' -a"

kasi@kasi-Inspiron-N5010 /media/kasi/Studies/CS 6200/cs6200sp17/assignment1 $ python web_crawler.py -s 'https://en.wikipedia.org/wiki/Sustainable_energy' -k 'solar' -o 'Task2B' -a
Created 'Task2B' directory to save crawl results
Crawled 251 links
Find the links crawled in 'links.txt' under 'Task2B' directory
Completed in 0:10:33.807948

6) For Task 3 enter the command "python web_crawler.py -s 'https://en.wikipedia.org/wiki/Solar_power' -o 'Task3'"

kasi@kasi-Inspiron-N5010 ~/Desktop $ python web_crawler_1.py -s 'https://en.wikipedia.org/wiki/Solar_power' -o 'Task3'
Created 'Task3' directory to save crawl results
Crawled 1000 links
Find the links crawled in 'links.txt' under 'Task3' directory
Completed in 0:29:41.737767
