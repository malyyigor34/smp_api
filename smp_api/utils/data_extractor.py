import extruct
import metadata_parser
from extract_social_media import find_links_tree
from html_to_etree import parse_html_bytes

from smp_api.Exceptions import WebSiteBlocked
from smp_api.utils.external_api.clearbit import get_logo_from_clearbit
from smp_api.utils.page_getters.browser import Browser
from smp_api.utils.page_getters.page_getter import PageGetter
from smp_api.utils.social_platforms_handlers.facebook.facebook import Facebook
from smp_api.utils.social_platforms_handlers.twitter_.twitter_ import TwitterHandler

BLOCKED_INDICATOR = ['Attemtion', 'Blocked',
                          'unauthorized', 'Locked',
                          'Unauthorised']


class DataExtractor:
    def __init__(self):
        self._twitter_handler = TwitterHandler()
        self._facebook_handler = Facebook()

    def _check_is_page_return_blocked_result(self, title: str) -> bool:
        for word in BLOCKED_INDICATOR:
            if title.lower().find(word.lower()) != -1:
                raise WebSiteBlocked
        return True

    def _get_page(self, url: str, via_browser: bool=True) -> str:
            # add try except
        if via_browser:
            self._page_getter = Browser()
        else:
            self._page_getter = PageGetter()

        res = self._page_getter.get_page(url)
        #title = self._page_getter.get_title()

        #self._check_is_page_return_blocked_result(title)
        return res

    def _get_links(self, res: str) -> dict:
        social_platforms_links = {}
        try:
            tree = parse_html_bytes(res.encode())
        except Exception:
            #log unknown
            return social_platforms_links
        for link in find_links_tree(tree):
            for social_platform in ['facebook.com', 'instagram.com', 'twitter.com']:
                try:
                    if link.find(social_platform) != -1:
                        social_platforms_links[social_platform] = link
                except AttributeError:
                    continue
                except Exception:
                    #log unknown error
                    continue
        return social_platforms_links

    def _get_metadata(self, res: str) -> dict:
        try:
            page = metadata_parser.MetadataParser(html=res)
        except Exception:
            #log unknown error
            return {}
        return page.metadata

    def _get_logo(self, url, page_source):
        logo = None
        try:
            logo = extruct.extract(page_source).get('json-ld', [{}])[0].get('logo')
            if not logo:
                logo = get_logo_from_clearbit(url)
        except Exception:
            #log unknown error
            return logo

    def extract(self, url: str) -> dict:
        page_source = self._get_page(url, via_browser=False)
        metadata = self._get_metadata(page_source)
        metadata['page']['logo'] = self._get_logo(url, page_source)
        links = self._get_links(page_source)
        twitter_data = self._twitter_handler.get_data(links.get('twitter.com'))
        facebook_data = self._facebook_handler.get_data(links.get('facebook.com'))
        return {
            'metadata': metadata,
            'links': links,
            'social':
            {
                'twitter': twitter_data,
                'facebook': facebook_data
            }
        }
