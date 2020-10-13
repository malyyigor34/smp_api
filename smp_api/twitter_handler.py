from twitter import Api
from twitter.error import *
from .AmazonBucket import upload_file, upload_image

def get_twitter_name(url):
    if url.find('twitter.com') != -1:
        return url.split('/')[-1]


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
        fields = ['name', 'description', 'followers_count', 'profile_image_url_https', 'profile_banner_url_https', 'profile_background_image_url_https',
                  'followers_count', 'friends_count', 'location']

        profile_details = {}

        for field in fields:
            try:
                profile_details[field] = upload_image(field, user.__getattribute__(field))
            except AttributeError:
                profile_details[field] = None
        return profile_details


