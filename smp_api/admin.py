from django.contrib import admin
from .models import Twitter, Cache, Proxy


class TwitterAdmin(admin.ModelAdmin):
    pass


class ChacheAdmin(admin.ModelAdmin):
    pass

class ProxyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Twitter, TwitterAdmin)
admin.site.register(Cache, ChacheAdmin)
#admin.site.register(Proxy, ProxyAdmin)