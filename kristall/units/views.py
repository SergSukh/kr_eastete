from datetime import datetime as dt
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from sorl.thumbnail import get_thumbnail

from .models import Unit, Citys, Streets, Buildings, Image, Published
from .forms import UnitCreateForm, ImagesFormSet, UnitForm


def pages(request, unit_list):
    units_in_page = settings.UNITS_IN_PAGE
    paginator = Paginator(unit_list, units_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    return render(request, 'units/index.html')


def units_list_show(request, units_list, title):
    for unit in units_list:
        print(unit)
        if unit.main_image():
            unit.img = get_thumbnail(
                unit.main_image(),
                "600x400",
                crop='top',
                upscale=True,
                quality=99
            )
    return render(
        request,
        'units/units_list.html',
        {'page_obj': pages(request, units_list), 'title': title}
    )


def units_list(request):
    if request.user.is_staff:
        units_list = Unit.objects.all()
    else:
        units_list = Unit.objects.filter(published__answer=True)
    return units_list_show(request, units_list, 'Объекты')


def units_rent(request):
    units_list = Unit.objects.filter(deal='Аренда')
    return units_list_show(request, units_list, 'Аренда объектов')


def units_sale(request):
    units_list = Unit.objects.filter(deal='Продажа')
    return units_list_show(request, units_list, 'Продажа объектов')


def unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    unit.imgs = []
    for img in unit.get_images():
        unit.imgs.append(
            get_thumbnail(
                img.image,
                "1200x900",
                crop='top',
                upscale=False,
                quality=99
            )
        )
    return render(request, 'units/unit_detail.html', {'unit': unit})


def save_images(unit, images):
    unit.images.all().delete()
    for i_form in images.cleaned_data:
        if i_form and not i_form['DELETE']:
            image = i_form['image']
            photo = Image(unit=unit, image=image)
            photo.save()


@login_required
def unit_publicate(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if unit.is_published():
        Published.objects.filter(unit=unit).delete()
    else:
        Published.objects.create(
            unit=unit,
            pub_date=dt.now())
    return redirect('units:unit_detail', unit_id)


@login_required
def unit_create(request, unit=None):
    form = UnitCreateForm(
            request.POST or None,
            instance=unit
        )
    images = ImagesFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=Image.objects.filter(unit=unit)
    )
    if not form.is_valid() or not images.is_valid():
        context = {
            'form': form,
            'images': images,
            'is_edit': True if unit else False
        }
        return render(request, 'units/unit_create.html', context)
    city = Citys.objects.get_or_create(city=form['c_field'].value())
    street = Streets.objects.get_or_create(street=form['s_field'].value())
    build = Buildings.objects.get_or_create(
        building=form['b_field'].value(),
        block=form['bl_field'].value(),
        floors=(
            form['f_field'].value() if type(form['f_field']) == int else None)
    )
    unit = form.save(commit=False)
    unit.author = request.user
    unit.city = city[0]
    unit.street = street[0]
    unit.build = build[0]
    unit.save()
    save_images(unit, images)
    return redirect('units:units_list')


@login_required
def unit_edit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if request.user.is_staff or unit.author == request.user:
        form = UnitForm(
            request.POST or None,
            instance=unit
        )
        images = ImagesFormSet(
            request.POST or None,
            request.FILES or None,
            queryset=Image.objects.filter(unit=unit)
        )
        if not form.is_valid() or not images.is_valid():
            context = {
                'form': form,
                'images': images,
                'is_edit': True if unit else False
            }
            return render(request, 'units/unit_create.html', context)
        unit = form.save()
        save_images(unit, images)
    return redirect('units:units_list')
