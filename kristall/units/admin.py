from django.contrib import admin

from .forms import ElementInLineFormSet
from .models import Unit, Image, Citys, Streets, Buildings


class UnitImagesInLine(admin.TabularInline):
    model = Image
    formset = ElementInLineFormSet
    extra = 1
    max_num = 20


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'square', 'city', 'is_published']
    inlines = [UnitImagesInLine]


@admin.register(Citys)
class CityAdmin(admin.ModelAdmin):
    list_display = ['city']


@admin.register(Streets)
class StreetAdmin(admin.ModelAdmin):
    list_display = ['street']


@admin.register(Buildings)
class BuildAdmin(admin.ModelAdmin):
    list_display = ['building', 'block', 'floors']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['unit', 'image']
