from django.urls import path

import views

app_name = 'units'

urlpatterns = [
    path('', views.index, name='index'),
    path('units_list/', views.units_list, name='units_list'),
    path('units_rent/', views.units_rent, name='units_rent'),
    path('units_sale/', views.units_sale, name='units_sale'),
    path('unit_detail/<int:unit_id>/', views.unit_detail, name='unit_detail'),
    path(
        'unit_publicate/<int:unit_id>/',
        views.unit_publicate,
        name='unit_publicate'
    ),
    path('create/', views.unit_create, name='unit_create'),
    path('m_create/', views.msg_create, name='msg_create'),
    path('unit/<int:unit_id>/edit/', views.unit_edit, name='unit_edit'),
]
