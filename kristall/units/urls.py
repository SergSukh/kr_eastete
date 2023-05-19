from django.urls import path

from .views import (index, units_list, unit_detail,
                    unit_edit, unit_create, unit_publicate,
                    units_rent, units_sale, msg_create)


app_name = 'units'


urlpatterns = [
    path('', index, name='index'),
    path('units_list/', units_list, name='units_list'),
    path('units_rent/', units_rent, name='units_rent'),
    path('units_sale/', units_sale, name='units_sale'),
    path('unit_detail/<int:unit_id>/', unit_detail, name='unit_detail'),
    path(
        'unit_publicate/<int:unit_id>/',
        unit_publicate,
        name='unit_publicate'
    ),
    path('create/', unit_create, name='unit_create'),
    path('m_create/', msg_create, name='msg_create'),
    path('unit/<int:unit_id>/edit/', unit_edit, name='unit_edit'),
]
