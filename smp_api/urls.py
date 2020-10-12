from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from .views import UrlHandler

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path(r'', UrlHandler.as_view())
]
