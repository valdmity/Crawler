from urllib.request import urlopen
from html_parser import Parser
from files_handler import *
from bs4 import BeautifulSoup
import threading


class Spider:

    project_name = ''
    base_url = ''
    domains = []
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    lock = threading.Lock()
    pages_by_links = {}


    def __init__(self, project_name: str, base_url: str, domain_name: list[str], save_type: str, limit: int):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domains = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.pages_directory = Spider.project_name + '/pages'
        Spider.save_type = save_type
        Spider.limit = limit

        self.prepare()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def prepare():
        create_directory(Spider.project_name)
        create_directory(Spider.pages_directory)
        create_data_files(Spider.project_name, Spider.base_url)
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
            parts = page_url.split('/') 
            name = parts[-1] if parts[-1] != '' else parts[-2]
            page_filename = Spider.pages_directory + '/' + name
            Spider.save_page_info(page_filename, html_code, page_url)
            links = Spider.gather_links(page_url, html_code)
            Spider.add_links_to_dict(links, page_filename)
            Spider.update_pages_by_link(page_url, page_filename)
            Spider.add_links_to_queue(links)
            print(page_url)
            print(Spider.pages_by_links[page_url])
        except Exception as exception:
            print(exception)


    @staticmethod
    def add_links_to_dict(links: list[str], page_filename: str):
        for link in links:
            if link not in Spider.pages_by_links:
                Spider.pages_by_links[link] = []
            Spider.pages_by_links[link].append(page_filename)

    @staticmethod
    def update_pages_by_link(link: str, page_filename: str):
        if link not in Spider.pages_by_links:
            return
        for path in Spider.pages_by_links[link]:
            data = read_from_file(path)
            data = data.replace(link, page_filename)
            delete_file_contents(path)
            write_to_file(path, data)

    @staticmethod
    def gather_links(page_url: str, html_code: str) -> set[str]:
        try:
            finder = Parser(Spider.base_url, page_url)
            finder.feed(html_code)
            return finder.page_links()
        except Exception as exception:
            raise exception


    @staticmethod
    def get_image_urls(html_code: str) -> set[str]:
        soup = BeautifulSoup(html_code, features="html.parser")
        return set([imgtag['src'] for imgtag in soup.find_all('img')])

    
    @staticmethod
    def get_image_by_url(url: str, page_url: str) -> bytes:
        print(url)
        if url.startswith('http'):
            res = urlopen(url)
        else:
            res = urlopen('https:' +  url)
        return res.read()

    
    @staticmethod
    def save_images(html_code: str, page_url: str):
        image_urls = Spider.get_image_urls(html_code)
        for url in image_urls:
            image = Spider.get_image_by_url(url, page_url)
            image_filename = Spider.pages_directory + '/' + 'img_' + url.split('/')[-1]
            if len(image) < Spider.limit:
                write_to_file_in_binary_mode(image_filename, image)



    @staticmethod
    def save_page_info(page_filename: str, html_code: str, page_url: str):
        match Spider.save_type:
            case 'html':
                write_to_file(page_filename, html_code)
            case 'image':
                Spider.save_images(html_code, page_url)



    @staticmethod
    def get_html_code(page_url: str) -> str:
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                return html_bytes.decode('utf-8')
            raise Exception('Page does not contain html code')
        except Exception as exception:
            raise exception

    @staticmethod
    def add_links_to_queue(links: set[str]):
        for url in links:
            if url in Spider.queue or url in Spider.crawled:
                continue
            if any([domain_name in url for domain_name in Spider.domains]):
                Spider.queue.add(url)

    @staticmethod
    def update_files():
        convert_set_to_file(Spider.queue, Spider.queue_file)
        convert_set_to_file(Spider.crawled, Spider.crawled_file)
