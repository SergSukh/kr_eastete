from django.urls import path

from .views import map_units_search, msg_create

app_name = 'service'

urlpatterns = [
    path('msg_create/', msg_create, name='msg_create'),
    path('units_search/', map_units_search, name='units_search'),
]
