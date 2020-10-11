from twitter import Api
from twitter.error import *
from .AmazonBucket import upload_file
import requests
import os
import tempfile
import random


def get_twitter_name(url):
    if url.find('twitter.com') != -1:
        return url.split('/')[-1]


def upload_image(key, value):
    if key.find('_url') != -1:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(requests.get(value).content)
            temp.flush()
            object_name = f'{random.randint(0,9999999)}.png'
            url = upload_file(temp.name, 'twitterimagies', object_name)
        return url
    return value

def auth(consumer_key, consumer_secret, access_token_secret,
                 access_token_key):
    try:
        api = Api(consumer_secret=consumer_secret, consumer_key=consumer_key,
                  access_token_secret=access_token_secret,
                  access_token_key=access_token_key)

        api.VerifyCredentials()
    except TwitterError:
        print('err')
        return False
    return api


def get_twitter_data(twitter_url, twitters_keys):
    try:
        twitter_url = get_twitter_name(twitter_url)
    except AttributeError:
        return
    for twitter_keys in twitters_keys:
        api = auth(**twitter_keys)
        if not api:
            continue
        if int(api.rate_limit.resources.get('account').get('/account/verify_credentials').get('remaining')) == 0:
            continue
        try:
            user = api.GetUser(screen_name=twitter_url)
        except TwitterError:
            try:
                user = api.GetUser(user_id=twitter_url)
            except TwitterError:
                user = None
        fields = ['followers_count', 'profile_image_url_https', 'profile_banner_url_https', 'profile_background_image_url_https',
                  'followers_count', 'friends_count', 'location']

        profile_details = {}

        for field in fields:
            try:
                profile_details[field] = upload_image(field, user.__getattribute__(field))
            except AttributeError:
                profile_details[field] = None
        return profile_details


#def upload_image(value):
#    if value.find('')

#get_twitter_data('https://twitter.com/AgataBlack1', [{
#    'consumer_secret': 'Lewou1qwAklSLj5i3iO9ij5NdpKyjPvQ0TKKW8Orvgq4R0kAvT',
#    'consumer_key': 'TG4OgtxtXDz6EZ4iJHXZXb0rk',
#    'access_token_secret': '447sYo6nnjrUuV4Ivj4eYApU9orHQxJRxFsGDh82ncJAa',
#    'access_token_key': '963002008188915713-t2VZgM0Jfa7zGAQNY9xdNMfT3ZxlyBH'
#}])
