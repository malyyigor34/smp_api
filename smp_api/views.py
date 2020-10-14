from rest_framework.views import APIView
from rest_framework.response import Response
from .data_extractor import get_data
from .validators import validate_url
from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.db.models import ObjectDoesNotExist
from .Exceptions import InvalidUrl, OldChache, WebSiteBlocked
from .models import Cache, Twitter, Proxy, TestUrl
import datetime
import os
import json
import requests


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
    def get(self, request):
        proxy_dict = {}
        try:
            fields = ['ip', 'port', 'login', 'password', 'is_fb', 'is_browser']
            proxy = Proxy.objects.all()[0]
            proxy_dict = {}
            for field in fields:
                proxy_dict[field] = proxy.__getattribute__(field)

        except (ObjectDoesNotExist, AttributeError):
            for field in fields:
                proxy_dict[field] = None

        url = request.GET.get('domain')
        if not url:
            return Response({'error': 'Give URL'})
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
            except WebSiteBlocked:
                response['error'] = f'{url} is blocked'
        response['data'] = data
        return Response(response)


class Test(APIView):
    def get(self, request):
        urls = TestUrl.objects.all()[0].urls.split('\n')
        server = '45.144.179.200:800/'
        ress = []
        for url in urls:
            url = url.replace('\r', '')
            ress.append({url: json.loads(requests.get(f'{server}?domain={url}').text)})
            i += 1
        return Response(ress)