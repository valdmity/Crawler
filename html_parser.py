from html.parser import HTMLParser
from urllib import parse


class Parser(HTMLParser):

    def __init__(self, base_url: str, page_url: str):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def error(self, message):
        print(message)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attr, value) in attrs:
                if attr == 'href':
                    url = parse.urljoin(self.base_url, value)
                    if 'results/pages/' not in url:
                        self.links.add(url.split('#')[0])

    def page_links(self) -> set[str]:
        return self.links
