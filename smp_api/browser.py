from selenium import webdriver
from selenium.webdriver.chrome.options import Options, DesiredCapabilities
from selenium.common.exceptions import WebDriverException
import os
import zipfile
try:
    from .Exceptions import InvalidUrl
except ImportError:
    from Exceptions import InvalidUrl


class Browser():
    def __init__(self, login: str = None, password: str = None, ip: str = None, port: str = None,
                 js_status=True):
        chrome_options = Options()
        exp_opt = {}
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
#        chrome_options.add_argument('--lang=en')
        #chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-webgl')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument("--lang=en")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument('user-agent={}'.format(user_agent))
        chrome_options.add_argument("--disable-javascript")
        #chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})


        if ip:
            manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

            background_js = """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """ % (ip, port, login, password)

            pluginfile = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)

        self.driver = webdriver.Chrome('smp_api/chromedriver', chrome_options=chrome_options)

    def get_page(self, url: str):
        if url.find('https') == -1 and url.find('http') ==-1:
            url = 'https://'+url
        try:
            self.driver.get(url)
        except WebDriverException:
            raise InvalidUrl(f"Can't access {url}")
        return self.driver.page_source
