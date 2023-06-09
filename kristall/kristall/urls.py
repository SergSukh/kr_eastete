from core.views import get_contact
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('units.urls', namespace='units')),
    path('service/', include('service.urls', namespace='service')),
    path('admin/', admin.site.urls),
    path('contact/', get_contact, name='contact'),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
