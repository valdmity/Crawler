import threading
from queue import Queue
from spider import Spider
from domains_handler import *
from files_handler import *


PROJECT_NAME = 'results'
HOMEPAGE = 'https://en.wikipedia.org/wiki/FC_Zenit_Saint_Petersburg'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 1

queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

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
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()