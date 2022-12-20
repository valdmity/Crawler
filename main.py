import threading
import sys
from queue import Queue
from spider import Spider
from domains_handler import *
from files_handler import *
import argparse


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-t', '--type', nargs='?', choices=['image', 'html'], \
    default='html', help='Краулер сохраняет файлы только выбранного типа')
arg_parser.add_argument('-u', '--url', nargs='?', type=str, default='https://habr.com/ru/all', \
    help='Стартовая ссылка Краулера')
arg_parser.add_argument('-l', '--limit', nargs='?', type=int, default=sys.maxsize, \
    help='Лимит на сохраниение в байтах, используется только для изображений')
arg_parser.add_argument('-n', '--number_threads', nargs='?', type=int, default=1)
args = arg_parser.parse_args()


PROJECT_NAME = 'results'
HOMEPAGE = args.url
DOMAINS = [get_domain_name(HOMEPAGE)]
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
NUMBER_OF_THREADS = args.number_threads

queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAINS, args.type, args.limit)


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=work)
        thread.daemon = True
        thread.start()


def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


def create_jobs():
    for link in convert_file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    queued_links = convert_file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
