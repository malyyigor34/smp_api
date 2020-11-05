import unittest

from smp_api.Exceptions import ValidationError, ErrorAtGettingPage
from smp_api import load_config
from smp_api.page_getter import PageGetter


class PageGetterTest(unittest.TestCase):
    def setUp(self) -> None:
        load_config()
        self._page_getter = PageGetter()

        self.urls_bad = {'xe.com1': ValidationError,
                     'https://xe.co1m': ValidationError,
                     'http1://xe.com': ValidationError}

        self.urls_good = {
                     'xe.com': str,
                     'https://xe.com': str,
                     'http://xe.com': str
                     }
        self.bad_url = 'xe.com1'
        self.good_url = 'xe.com'

    def test_get_page_bad(self):
        for url, result in self.urls_bad.items():
            with self.assertRaises(result) as context:
                res = self._page_getter.get_page(url)
                self.assertTrue('This is broken' in context.exception)

    def test_page_good(self):
        for url, result in self.urls_good.items():
            self.assertIsInstance(self._page_getter.get_page(url), result)
#            print(url)

    def test_get_title_bad(self):
        with self.assertRaises(ErrorAtGettingPage) as context:
            self._page_getter.get_title()
            self.assertTrue('This is broken' in context.exception)

    def test_get_title_good(self):
        self.assertIsInstance(self._page_getter.get_page(self.good_url), str)


if __name__ == '__main__':
    unittest.main()
