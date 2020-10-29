import os

import requests
from bs4 import BeautifulSoup

from smp_api.utils.Exceptions import ErrorAtGettingPage, BadConfigurated
from smp_api.utils.common_modules.common import validate_url
from smp_api.utils.config import load_config


class PageGetter:
    def __init__(self):
        self._page_content = None
        try:
            self._page_getter_api_url = os.environ['PAGE_GETTER_API_URL']
            self._page_getter_api_key = os.environ['PAGE_GETTER_API_KEY']
            self._page_getter_api_key_name = os.environ['PAGE_GETTER_API_KEY_NAME']
            self._page_getter_api_url_name = os.environ['PAGE_GETTER_API_URL_NAME']
            self._page_getter_request_type = os.environ['PAGE_GETTER_REQUEST_TYPE']
        except (AttributeError, KeyError):
            raise BadConfigurated('Error in page getter configuration. Check CONFIG.py')
            #log

    def get_page(self, url):
        url = validate_url(url)
        try:
            if self._page_getter_request_type == 'GET':
                requested_url = f'{self._page_getter_api_url}?{self._page_getter_api_key_name}={self._page_getter_api_key}&' \
                                f'{self._page_getter_api_url_name}={url}'

                page = requests.get(requested_url)
                self._page_content = page.text
            else:
                page = requests.post(self._page_getter_api_url, data={
                    self._page_getter_api_key_name: self._page_getter_api_key,
                    self._page_getter_api_url_name: url,
                    'jsrender': 'true',
                    'renderuntil': 'domloaded',
                    'countrycodes': ['uk', 'us'],
                    'loadall': 'true',
                    'proxytype': 'residential',
                })
                self._page_content = page.json().get(os.environ.get('PAGE_GETTER_CONTENT_CONTAINER'))
            if page.status_code != 200:
                print(page.text)
                raise ErrorAtGettingPage(page.text)
            return self._page_content
        except requests.exceptions.RequestException:
            raise ErrorAtGettingPage(f'Error at request to url {url}')
            #log

    def get_title(self):
        try:
            soup = BeautifulSoup(self._page_content)
        except TypeError:
            #log page not getted
            raise ErrorAtGettingPage('Page not getted.')
        return soup.find('title').text


if __name__ == '__main__':
    load_config()
    p = PageGetter()
    print(p.get_page('xe.com'))