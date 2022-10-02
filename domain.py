from urllib import urlparse


def get_domain_name(url: str) -> str:
    try:
        res = get_sub_domain_name(url).split('.')
        return '.'.join(res[-2], res[-1])
    except:
        return ''

def get_sub_domain_name(url: str) -> str:
    try:
        return urlparse(url).netloc
    except:
        return ''