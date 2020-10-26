
import json

import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from smp_api.utils.data_extractor_manager import DataExtractorManager
from .models import TestUrl, Twitter
from .serializers import TwitterSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class UrlHandler(APIView):
    @method_decorator(cache_page(60 * 60 * 50))
    def get(self, request):
        url = request.GET.get('domain')
        if not url:
            return Response({'error': 'Give URL'})
        response = DataExtractorManager(url).get()
        return Response(response)


class TwitterKeys(APIView):
    def get(self, request):
        return Response(TwitterSerializer(Twitter.objects.all(), many=True).data)


class Test(APIView):
    def get(self, request):
        urls = TestUrl.objects.all()[0].urls.split('\n')
        server = 'http://45.144.179.200:800/'
        ress = []
        for url in urls:
            url = url.replace('\r', '')
            ress.append({url: json.loads(requests.get(f'{server}?domain={url}').text)})
        return Response(ress)

