import os

import requests

from smp_api.utils.config.load_config import load_config


class TwitterKeys():
    def __init__(self):
        self._keys = requests.get(f"{os.environ.get('APP_PROTOCOL')}://{os.environ.get('APP_URL')}"
                     f":{os.environ.get('APP_PORT')}/{os.environ.get('TWITTER_KEYS_API_ENDPOINT')}").json()

    def get(self):
        return self._keys


if __name__ == '__main__':
    load_config()
    t = TwitterKeys()


