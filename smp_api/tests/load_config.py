import os

from CONFIG import CONFIG


def load_config():
    for key, value in CONFIG.items():
        os.environ.update({key: str(value)})
