from django.urls import path

import .view


app_name = 'units'

urlpatterns = [
    path('', view.index, name='index'),
    path('units_list/', view.units_list, name='units_list'),
    path('units_rent/', view.units_rent, name='units_rent'),
    path('units_sale/', view.units_sale, name='units_sale'),
    path('unit_detail/<int:unit_id>/', view.unit_detail, name='unit_detail'),
    path(
        'unit_publicate/<int:unit_id>/',
        view.unit_publicate,
        name='unit_publicate'
    ),
    path('create/', view.unit_create, name='unit_create'),
    path('m_create/', view.msg_create, name='msg_create'),
    path('unit/<int:unit_id>/edit/', view.unit_edit, name='unit_edit'),
]
