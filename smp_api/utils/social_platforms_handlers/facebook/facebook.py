import time
import os
from bs4 import BeautifulSoup

from smp_api.utils.amazon_bucket import upload_image
from smp_api.utils.page_getters.browser import Browser
from smp_api.utils.page_getters.page_getter import PageGetter
from smp_api.utils.config.load_config import load_config
import tempfile
class Facebook():
    def __init__(self, via_browser=False):
        self._via_browser = via_browser

    def _accept_banner(self, soup, browser):
        try:
            for element in soup.find_all():
                if element.attrs.get('data-testid') == 'cookie-policy-banner-accept':
                    browser.driver.find_element_by_id(element.attrs.get('id')).click()
        except Exception:
            pass

    def get_data(self, url):
        if self._via_browser:
            data = self._get_data_via_browser(url)
        else:
            data = self._get_data_via_pg(url)
        return data

    def _get_data_via_pg(self, url):
        logo = None
        banner = None
        description = None
        name = None
       # try:
        page_getter = PageGetter()
        page_source = page_getter.get_page(url)

        browser = Browser()

        with open('tmp.html', 'w') as f:
            f.write(page_source)
        page_source = browser.get_page_from_file('file:///'+os.path.realpath('tmp.html'))
        time.sleep(1)

        soup = BeautifulSoup(page_source)

        try:
            name = soup.find('h1').find('span').text
        except AttributeError:
            name = None
        try:
            banner = soup.find('img', {'class': '_4on7 _3mk2 _8f5u img'}).attrs.get('src')
        except AttributeError:
            try:
                banner = soup.find('video').attrs.get('src')
            except AttributeError:
                banner = None

        logo = None
        for elem in soup.find_all():
            if elem.attrs.get('aria-label') == 'Profile picture':
                logo = elem.find('img').attrs.get('src')

        page_source = page_getter.get_page(url.replace('facebook.com/', 'facebook.com/pg/') + 'about')
        soup = BeautifulSoup(page_source)


        try:
            description = list(
                filter(lambda div: div.text.find('About') != -1, soup.find_all('div', {'class': '_4bl9'})))
            description = description[1].text.replace('About', '')
            # except IndexError:
            #    description = None

        except Exception:
            pass
#        except Exception:
#            pass
        print()
        return {
            'description': description,
            'name': name,
            'logo_url': upload_image('logo_url', logo),
            'banner_url': upload_image('banner_url', banner)
        }

    def _get_data_via_browser(self, url):
        logo = None
        banner = None
        description = None
        name = None
        try:
            browser = Browser()
            page_source = browser.get_page(url)
            time.sleep(0.5)
            soup = BeautifulSoup(page_source)

            self._accept_banner(soup, browser)
            soup = BeautifulSoup(browser.driver.page_source)
            try:
                name = soup.find('h1').find('span').text
            except AttributeError:
                name = None
            try:
                banner = soup.find('img', {'class': '_4on7 _3mk2 _8f5u img'}).attrs.get('src')
            except AttributeError:
                try:
                    banner = soup.find('video').attrs.get('src')
                except AttributeError:
                    banner = None

            logo = None
            for elem in soup.find_all():
                if elem.attrs.get('aria-label') == 'Profile picture':
                    logo = elem.find('img').attrs.get('src')

            page_source = browser.get_page(url.replace('facebook.com/', 'facebook.com/pg/') + '/about')
            time.sleep(0.1)

            soup = BeautifulSoup(page_source)
            self._accept_banner(soup, browser)

            soup = BeautifulSoup(browser.driver.page_source)

            try:
                description = list(filter(lambda div: div.text.find('About') != -1, soup.find_all('div', {'class': '_4bl9'})))
                description = description[1].text.replace('About', '')
                #except IndexError:
                #    description = None

            except Exception:
                pass
        except Exception:
            pass
        return {
            'description': description,
            'name': name,
            'logo_url': upload_image('logo_url', logo),
            'banner_url': upload_image('banner_url', banner)
        }


if __name__ == '__main__':
    load_config()
    p = Facebook()
    data = p._get_data_via_pg('https://www.facebook.com/ASOS/')
    print(data)