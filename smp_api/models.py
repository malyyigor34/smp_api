from django.db.models import *
from datetime import datetime


class Cache(Model):
    domain = CharField(max_length=250)
    data = CharField(max_length=85000)
    date = FloatField()

    def __str__(self):
        return f'{self.domain} - {datetime.fromtimestamp(self.date)}'


class Twitter(Model):
    name = CharField(max_length=250, help_text='Set name for this pair API keys')
    access_token_key = CharField(max_length=500)
    access_token_secret = CharField(max_length=500)
    consumer_key = CharField(max_length=500)
    consumer_secret = CharField(max_length=500)

    def __str__(self):
        return f'{self.name} - {self.access_token_key}'


class TestUrl(Model):
    urls = TextField(max_length=25000)


class Proxy(Model):
    ip = CharField(max_length=400)
    port = CharField(max_length=60)
    login = CharField(max_length=150, blank=True)
    password = CharField(max_length=150, blank=True)

    is_fb = BooleanField(default=True)
    is_browser = BooleanField(default=True)


    def __str__(self):
        return f'{self.ip}:{self.port}. For FB: {self.is_fb}; for browser: {self.is_browser}'
