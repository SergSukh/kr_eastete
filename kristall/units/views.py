from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator

from .models import Unit
from .forms import UnitForm, CitysForm, StreetsForm, BuildingsForm, FlatsForm


def pages(request, unit_list):
    units_in_page = settings.UNITS_IN_PAGE
    paginator = Paginator(unit_list, units_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    return render(request, 'units/index.html')


def units_list(request):
    units_list = Unit.objects.all()
    return render(
        request,
        'units/units_list.html',
        {'page_obj': pages(request, units_list)}
    )


@login_required
def create_unit(request, unit=None):
    forms = [
        UnitForm(request.POST or None, instance=unit),
        CitysForm(request.Post or None, instance=unit.adress.city),
        StreetsForm(request.Post or None, instance=unit.adress.street),
        BuildingsForm(request.Post or None, instance=unit.adress.building),
        FlatsForm(request.Post or None, instance=unit.adress.flats)
    ]
    for form in forms:
        if not form.is_valid():
            context = {
                'forms': forms,
                'is_edit': True if unit else False
            }
            return render(request, 'units/unit_create.html', context)
        form.save()
        return redirect(request, 'units/units_list')


@login_required
def units_edit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if request.user.role == 'moderator' or request.user.role == 'admin':
        return create_unit(request, unit)
    return redirect(request, 'units/units_list')
