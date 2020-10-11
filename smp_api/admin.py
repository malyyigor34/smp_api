from django.contrib import admin
from .models import Twitter, Cache


class TwitterAdmin(admin.ModelAdmin):
    pass


class ChacheAdmin(admin.ModelAdmin):
    pass


admin.site.register(Twitter, TwitterAdmin)
admin.site.register(Cache, ChacheAdmin)