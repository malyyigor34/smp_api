from validator_collection import checkers

from smp_api.Exceptions import ValidationError


def validate_url(url):
    if url.find('http://') == -1 and url.find('https://') == -1:
        url = 'https://' + url
    if not checkers.is_url(url):
        #  log inc url
        raise ValidationError(f'{url} is incorrect url')
    return url