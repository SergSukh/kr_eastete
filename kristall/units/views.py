from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator

from .models import Unit


def pages(request, unit_list):
    units_in_page = settings.UNITS_IN_PAGE
    paginator = Paginator(unit_list, units_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    units_list = Unit.objects.all()
    context = {
        'page_obj': pages(request, units_list),
    }
    return render(request, 'units/index.html', context)


@login_required
def create_unit(request):
    pass
