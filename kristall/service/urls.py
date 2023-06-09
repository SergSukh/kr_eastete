from django.urls import path

from .views import feedback, msg_create

app_name = 'service'

urlpatterns = [
    path('msg_create/', msg_create, name='msg_create'),
    path('feedback/', feedback, name='feedback'),
]
