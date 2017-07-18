from django.contrib import admin

from .models import Main, Yangjin, Yangsung, Crj

@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    pass


@admin.register(Yangsung)
class YangsungAdmin(admin.ModelAdmin):
    pass


@admin.register(Yangjin)
class YangjinAdmin(admin.ModelAdmin):
    pass


@admin.register(Crj)
class CrjAdmin(admin.ModelAdmin):
    pass
