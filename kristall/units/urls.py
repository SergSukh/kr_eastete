from django.urls import path

from .views import index


app_name = 'units'


urlpatterns = [
    path('', index, name='index'),
]
