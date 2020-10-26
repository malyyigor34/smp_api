from twitter import Api
from twitter.error import *

from smp_api.utils.amazon_bucket import upload_image
from smp_api.utils.config.load_config import load_config
from smp_api.utils.social_platforms_handlers.twitter_.keys import TwitterKeys


class TwitterHandler:
    def __init__(self):
        self._twitters_keys = TwitterKeys().get()

    def _get_twitter_name(self, url: str) -> str:
            if url.find('twitter.com') != -1:
                return url.split('/')[-1]

    def _auth(self, consumer_key: str, consumer_secret: str, access_token_secret: str,
                     access_token_key: str) -> Api:
        try:
            api = Api(consumer_secret=consumer_secret, consumer_key=consumer_key,
                      access_token_secret=access_token_secret,
                      access_token_key=access_token_key)

            api.VerifyCredentials()
        except TwitterError:
            #log error at auth
            return False
        except Exception:
            return False
            #log unexpected err
        return api

    def get_data(self, twitter_url):
        try:
            twitter_url = self._get_twitter_name(twitter_url)
        except AttributeError:
            #log
            return {}
            #raise TwitterProfileNotFound
        for twitter_keys in self._twitters_keys:
            api = self._auth(**twitter_keys)
            if not api:
                continue
            if int(api.rate_limit.resources.get('account').get('/account/verify_credentials').get('remaining')) == 0:
                #log no limits
                continue
            try:
                user = api.GetUser(screen_name=twitter_url)
            except TwitterError:
                try:
                    user = api.GetUser(user_id=twitter_url)
                except TwitterError:
                    user = None

            fields = ['name', 'description', 'followers_count', 'profile_image_url_https', 'profile_banner_url_https',
             'profile_background_image_url_https',
             'followers_count', 'friends_count', 'location']

            profile_details = {}

            for field in fields:
                try:
                    profile_details[field] = upload_image(field, user.__getattribute__(field))
                except AttributeError:
                    profile_details[field] = None
                    #log profile field not found
            return profile_details


if __name__ == '__main__':
    load_config()
    t = TwitterHandler()
    print(t.get_data('https://twitter.com/xecom'))