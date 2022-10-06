from urllib.parse import urlparse


def get_domain_name(url: str) -> str:
    try:
        res = get_sub_domain_name(url).split('.')
        print('.'.join([res[-2], res[-1]]))
        return '.'.join([res[-2], res[-1]])
    except Exception as exception:
        print(exception)
        return ''

def get_sub_domain_name(url: str) -> str:
    try:
        return urlparse(url).netloc
    except Exception as exception:
        print(exception)
        return ''