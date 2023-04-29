from django.urls import path

from .views import index, units_list


app_name = 'units'


urlpatterns = [
    path('', index, name='index'),
    path('units_list/', units_list, name='units_list'),
]
