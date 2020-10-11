from rest_framework import serializers
from .models import Twitter

class TwitterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twitter
        fields = ['consumer_secret', 'consumer_key', 'access_token_secret',
                  'access_token_key']