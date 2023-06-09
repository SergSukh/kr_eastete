from django.conf import settings
from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'core/500.html', {'path': request.path}, status=500)


def csrf_error(request, exections):
    return render(request, 'core/403.html', {'path': request.path}, status=403)


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')


def get_contact(request):
    return render(
        request,
        'core/contact.html',
        {'YandexMapsAPI': settings.YANDEX_MAPS_API}
    )
