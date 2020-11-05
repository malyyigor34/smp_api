import unittest
from unittest.mock import patch

from smp_api import load_config
from smp_api.data_extractor import DataExtractor


class DataExtractorTest(unittest.TestCase):
    def setUp(self) -> None:
        load_config()
        self.url = 'xe.com'
        self._data_extractor = DataExtractor()
        with patch('requests.get') as r_mock:
            instance = r_mock.return_value
            instance.get.return_value = """
            <html><head><title>Blocked</title></head><body>sf</body></html>"""

    def check_is_page_return_blocked_result_test(self):
        self.assertIsInstance(self._data_extractor._check_is_page_return_blocked_result('BlockeD'), bool)

    def get_page_via_browser_test(self):
        pass

    def test_get_page_via_api(self):
        res = self._data_extractor._get_page('xe.com', via_browser=False)
        self.assertIsInstance(res, str)

    def test_get_links(self):
        with open('data_for_tests/page_with_social_media.html', 'r') as f:
            page = f.read()
        res = self._data_extractor._get_links(page)
        self.assertEqual(res.get('facebook.com'), 'https://www.facebook.com/HelloFreshus')

    def get_metadata_test(self):
        pass

    def get_logo_test(self):
        pass

    def extract_test(self):
        pass
