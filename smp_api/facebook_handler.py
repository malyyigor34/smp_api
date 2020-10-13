from .browser import Browser
from bs4 import BeautifulSoup
import time
import random
from .AmazonBucket import upload_image


def accept_banner(soup, browser):
    try:
        for element in soup.find_all():
            if element.attrs.get('data-testid') == 'cookie-policy-banner-accept':
                browser.driver.find_element_by_id(element.attrs.get('id')).click()
    except Exception:
        pass


def get_facebook_data(url):
    logo = None
    banner = None
    description = None
    name = None
  # try:
    browser = Browser()
    page_source = browser.get_page(url)
    time.sleep(0.5)
    soup = BeautifulSoup(page_source)

    accept_banner(soup, browser)
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
    accept_banner(soup, browser)

    soup = BeautifulSoup(browser.driver.page_source)

    try:
        description = list(filter(lambda div: div.text.find('About') != -1, soup.find_all('div', {'class': '_4bl9'})))
        description = description[1].text.replace('About', '')
        #except IndexError:
        #    description = None

    except Exception:
        pass

    return {
        'description': description,
        'name': name,
        'logo_url': upload_image('logo_url', logo),
        'banner_url': upload_image('banner_url', banner)
    }
