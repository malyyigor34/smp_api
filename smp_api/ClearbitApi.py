import requests
from .AmazonBucket import upload_image
import os


def get_logo(url):
    url = url.replace('https://', '')
    url = url.replace('http://', '')

    logo = requests.get('https://logo.clearbit.com/'+url)

    return upload_image('logo_url', None, request_inst=logo)


if __name__ == '__main__':
    os.environ.update({'BUCKET_NAME': 'twitterimagies'})
    get_logo('www.publicdesire.com')