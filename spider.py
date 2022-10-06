from urllib.request import urlopen
from parser import Parser
from files_handler import *
import threading


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    lock = threading.Lock()


    def __init__(self, project_name: str, base_url: str, domain_name: str):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.pages_directory = Spider.project_name + '/pages'
        self.prepare()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def prepare():
        create_directory(Spider.project_name)
        create_directory(Spider.pages_directory)
        create_data_files(Spider.project_name, Spider.base_url)
        with Spider.lock:
            Spider.queue = convert_file_to_set(Spider.queue_file)
            Spider.crawled = convert_file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name: str, page_url: str):
        if page_url not in Spider.crawled:
            print(thread_name + ' is crawling ' + page_url)
            print(' | '.join(['Queue: ' + str(len(Spider.queue)), 
            'Crawled: ' + str(len(Spider.crawled))]))
            with Spider.lock:
                Spider.parse_page(page_url)
                Spider.queue.remove(page_url)
                Spider.crawled.add(page_url)
                Spider.update_files()

    @staticmethod
    def parse_page(page_url: str):
        try:
            html_code = Spider.get_html_code(page_url)
            write_to_file(Spider.pages_directory + '/' + page_url.split('/')[-1], html_code)
            links = Spider.gather_links(page_url, html_code)
            Spider.add_links_to_queue(links)
        except Exception as exception:
            print(exception)


    @staticmethod
    def gather_links(page_url: str, html_code: str) -> set[str]:
        try:
            finder = Parser(Spider.base_url, page_url)
            finder.feed(html_code)
            return finder.page_links()
        except:
            raise

    @staticmethod
    def get_html_code(page_url: str) -> str:
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                return html_bytes.decode('utf-8')
            raise Exception('Page does not contain html code')
        except:
            raise

    @staticmethod
    def add_links_to_queue(links: set[str]):
        for url in links:
            if url in Spider.queue or url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        convert_set_to_file(Spider.queue, Spider.queue_file)
        convert_set_to_file(Spider.crawled, Spider.crawled_file)
    