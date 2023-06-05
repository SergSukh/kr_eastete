from django.urls import path

from .views import msg_create

app_name = 'service'

urlpatterns = [
    path('msg_create/', msg_create, name='msg_create'),
]
