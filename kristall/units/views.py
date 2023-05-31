from datetime import datetime as dt
from typing import Any

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import (get_object_or_404,
                              redirect, render)
from django.views.generic import TemplateView, ListView
from sorl.thumbnail import get_thumbnail

from .forms import ImagesFormSet, MessageForm, UnitCreateForm, UnitForm
from .models import Buildings, Citys, Image, Published, Streets, Unit


class IndexPageView(TemplateView):
    template_name = 'units/index.html'


def pages(request, unit_list):
    units_in_page = settings.UNITS_IN_PAGE
    paginator = Paginator(unit_list, units_in_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def units_list_show(request, objs_list, title):
    if not request.user.is_staff:
        objs_list = objs_list.filter(published__answer=True)
    for unit in objs_list:
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
        {'page_obj': pages(request, objs_list), 'title': title}
    )


def units_list(request):
    objs = Unit.objects.all()
    return units_list_show(request, objs, 'Объекты')


def units_rent(request):
    objs = Unit.objects.filter(deal='Аренда')
    return units_list_show(request, objs, 'Аренда объектов')


def units_sale(request):
    objs = Unit.objects.filter(deal='Продажа')
    return units_list_show(request, objs, 'Продажа объектов')


def get_search_min_param(param):
    return (float(param) if param else 0)


def get_search_max_param(param):
    return (float(param) if param else 999999999)


def search_units(request):
    deal = request.GET.get('deal')
    name = request.GET.get('q')
    if request.user.is_staff:
        public = None if request.GET.get('public') else True
    else:
        public = True
    sq_min = get_search_min_param(request.GET.get('sq_min'))
    sq_max = get_search_max_param(request.GET.get('sq_max'))
    pr_min = get_search_min_param(request.GET.get('pr_min'))
    pr_max = get_search_max_param(request.GET.get('pr_max'))
    objs = Unit.objects.filter(
        Q(published__answer=public),
        Q(deal__iregex=deal)|
        Q(name__iregex=name),
        Q(street__street__icontains=request.GET.get('street'))
    )
    obj_list = []
    for obj in objs:
        if obj.check_square(sq_min, sq_max) and obj.check_price(pr_min, pr_max):
            obj_list.append(obj)
    return units_list_show(request, objs, 'Объекты по запросу')

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
        pub = get_object_or_404(Published, unit=unit)
        pub.delete()
    else:
        pub = Published()
        pub.unit=unit
        pub.pub_date=dt.now()
        pub.answer = True
        pub.save()
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


def msg_create(request):
    form = MessageForm(request.Post or None)
    if form.is_valid():
        form.save()
        return redirect('units:units_list')
    return render(request, 'units/index.html', {'m_form': form})
