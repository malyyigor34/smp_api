from extract_social_media import find_links_tree
from html_to_etree import parse_html_bytes
from .browser import Browser
import metadata_parser
from .twitter_handler import get_twitter_data
import time
import extruct
from .facebook_handler import get_facebook_data
from .ClearbitApi import get_logo

def get_page(url):
    browser = Browser()
    res = browser.get_page(url)
    browser.driver.save_screenshot('1.png')
    return res


def get_links(res: str) -> dict:
    tree = parse_html_bytes(res.encode())
    social_platforms = ['facebook.com', 'instagram.com', 'twitter.com']
    social_platforms_links = {}
    for link in find_links_tree(tree):
        for social_platform in social_platforms:
            if link.find(social_platform) != -1:
                social_platforms_links[social_platform] = link
    return social_platforms_links


def get_metadata(res):
    page = metadata_parser.MetadataParser(html=res)
    return page.metadata


def get_data(url, twitters_keys):
    page_source = get_page(url)
    metadata = get_metadata(page_source)
    try:
        metadata['page']['logo'] = extruct.extract(page_source).get('json-ld', [])[0].get('logo')
    except Exception:
        try:
            metadata['page']['logo'] = get_logo(url)
        except Exception:
            metadata['page']['logo'] = None

    links = get_links(page_source)
    twitter_data = get_twitter_data(links.get('twitter.com'), twitters_keys)
    facebook_data = get_facebook_data(links.get('facebook.com'))
    return {
        'metadata': metadata,
        'links': links,
        'social':
        {
            'twitter': twitter_data,
            'facebook': facebook_data
        }
    }

