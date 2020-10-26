import os

from smp_api.utils.amazon_bucket import upload_image


def get_logo_from_clearbit(url):
    url = url.replace('https://', '')
    url = url.replace('http://', '')

    return upload_image('logo_url', 'https://logo.clearbit.com/'+url)


if __name__ == '__main__':
    os.environ.update({'BUCKET_NAME': 'twitterimagies'})
    get_logo_from_clearbit('www.publicdesire.com')