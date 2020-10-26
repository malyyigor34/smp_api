from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import UrlHandler, Test, TwitterKeys

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path(r'', UrlHandler.as_view()),
    path('test/', Test.as_view()),
    path('twitter_keys/', TwitterKeys.as_view())
]
