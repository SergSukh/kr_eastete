from django.contrib import admin
from .models import Unit, Adress, Citys, Streets, Buildings, Flats, Image



@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'square', 'is_published']


@admin.register(Adress)
class AdressAdmin(admin.ModelAdmin):
    list_display = ['city', 'street', 'building', 'flat']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['unit', 'image']
