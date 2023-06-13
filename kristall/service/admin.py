from django.contrib import admin

from .models import Ip, Post, UnitVisits, UserIp


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ['ip', 'description']


@admin.register(UserIp)
class UserIpAdmin(admin.ModelAdmin):
    list_display = ['user', 'visits']


@admin.register(UnitVisits)
class UnitVisitsAdmin(admin.ModelAdmin):
    list_display = ['unit', 'views', 'dt']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['mark', 'text', 'author', 'ip', 'pub_date']
