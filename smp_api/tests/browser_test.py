import unittest
from unittest.mock import patch

from browser import Browser
from load_config import load_config


class BrowserTest(unittest.TestCase):
    def setUp(self) -> None:
        load_config()

    def test_browser_creating(self):
        browser = Browser()
        self.assertIsInstance(browser, Browser)

    def test_browser_set_html(self):
        browser = Browser()
        page_source_test = """
            <html>
                 <head></head>
                 <body>
                     <div>
                         Hello World =)
                     </div>
                 </body>
            </html>
            """

        res = browser.open_page_from_string(page_source_test)
        self.assertEquals(res, page_source_test)

    def test_get_page(self):
        browser = Browser()
        res = browser.get_page('xe.com')
        self.assertIsInstance(res, str)