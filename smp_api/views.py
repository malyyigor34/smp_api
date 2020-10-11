from rest_framework.views import APIView
from rest_framework.response import Response
from .data_extractor import get_data
from .validators import validate_url
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.db.models import ObjectDoesNotExist
from .Exceptions import InvalidUrl, OldChache
from .models import Cache, Twitter
import datetime
import os
import json


def get_chache(url):
    try:
        try:
            response = Cache.objects.get(domain=url)
        except MultipleObjectsReturned:
            Cache.objects.all().delete()
            raise OldChache
        if datetime.datetime.now().timestamp() - response.date > float(os.environ.get('CACHE_LIFETIME'))*60:
            response.delete()
            raise OldChache
        else:
            return json.loads(response.data)
    except ObjectDoesNotExist:
        raise OldChache


def add_chache(url, data):
    data = json.dumps(data)
    Cache.objects.create(data=data, domain=url, date=datetime.datetime.now().timestamp())


def get_twitter_keys():
    keys = Twitter.objects.all()
    twitters_keys = []
    for key in keys:
        twitters_keys.append({
            'consumer_secret': key.consumer_secret,
            'consumer_key': key.consumer_key,
            'access_token_secret': key.access_token_secret,
            'access_token_key': key.access_token_key
        })
    return twitters_keys


class UrlHandler(APIView):
    def get(self, request, url):
        response = {'error': False, 'cached': False}
        data = None
        try:
            data = get_chache(url)
            response['cached'] = True
        except OldChache:
            try:
                validate_url(url)
            except ValidationError as e:
                response['error'] = e.message
                return Response(response)

            try:
                data = get_data(url, get_twitter_keys())
                add_chache(url, data)
            except InvalidUrl as e:
                response['error'] = e.message
        response['data'] = data
        return Response(response)
