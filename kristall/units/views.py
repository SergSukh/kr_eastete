from datetime import datetime as dt

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import (get_object_or_404,
                              redirect, render)
from sorl.thumbnail import get_thumbnail

from service.views import pages, save_ip, save_unit_ip, save_user_ip
from .forms import ImagesFormSet, UnitCreateForm, UnitEditForm
from .models import Buildings, Citys, Image, Published, Special, Streets, Unit


def get_image(self):
    if self.main_image():
        return get_thumbnail(
            self.main_image(),
            "600x400",
            crop='top',
            upscale=True,
            quality=99
        )
    return None

def units_list_show(request, objs_list, title):
    if not request.user.is_staff:
        objs_list = objs_list.filter(published__answer=True)
    for unit in objs_list:
        unit.img = get_image(unit)
    req = ''
    for q in request.GET:
        if q != 'page':
            req += f'&{q}={request.GET[q]}'
    return render(
        request,
        'units/units_list.html',
        {'page_obj': pages(request, objs_list), 'req': req, 'title': title}
    )


def index(request):
    save_ip(request)
    save_user_ip(request)
    object_list = Unit.objects.filter(
        published__answer=True,
        special__answer=True
    )
    for unit in object_list:
        unit.img = get_image(unit)
    return render(request, 'units/index.html', {'object_list': object_list[:2]})


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
        Q(deal__iregex=deal),
        Q(name__iregex=name),
        Q(published__answer=public),
        Q(street__street__icontains=request.GET.get('street'))
    )
    obj_list = []
    for obj in objs:
        if (
            obj.check_param(sq_min, obj.square, sq_max) and
            obj.check_param(pr_min, obj.price, pr_max)
        ):
            obj_list.append(obj)
    return units_list_show(request, objs, 'Объекты по запросу')


def unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    save_unit_ip(request, unit)
    unit.count_vizitors = unit.visits.count()
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
    return render(
        request,
        'units/unit_detail.html',
        {'unit': unit, 'YandexMapsAPI': settings.YANDEX_MAPS_API}
    )


def save_images(unit, images):
    unit.images.all().delete()
    for i_form in images.cleaned_data:
        if i_form and not i_form['DELETE']:
            image = i_form['image']
            Image.objects.create(unit=unit, image=image)


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
def unit_special(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if unit.is_special():
        pub = get_object_or_404(Special, unit=unit)
        pub.delete()
    else:
        pub = Special()
        pub.unit=unit
        pub.pub_date=dt.now()
        pub.answer = True
        pub.save()
    return redirect('units:unit_detail', unit_id)


@login_required
def unit_create(request, unit=None):
    form = UnitCreateForm(
        request.POST or None,
        request.FILES or None,
        instance=unit
    )
    images = (
        request.FILES.getlist('images') or None
    )
    if not form.is_valid():
        context = {
            'form': form,
            'images': images,
            'is_edit': False
        }
        return render(request, 'units/unit_create.html', context)
    city = Citys.objects.get_or_create(city=form['c_field'].value())
    street = Streets.objects.get_or_create(street=form['s_field'].value())
    build = Buildings.objects.get_or_create(
        building=form['b_field'].value(),
        block=form['bl_field'].value(),
        floors=(
            form['f_field'].value() if type(form['f_field']) == int else None
    ))
    unit = form.save(commit=False)
    unit.author = request.user
    unit.city = city[0]
    unit.street = street[0]
    unit.build = build[0]
    unit.save()
    for i_form in images:
        Image.objects.create(unit=unit, image=i_form)
    return redirect('units:units_list')


@login_required
def unit_edit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    if request.user.is_staff or unit.author == request.user:
        form = UnitEditForm(
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
                'is_edit': True
            }
            return render(request, 'units/unit_create.html', context)
        unit = form.save()
        save_images(unit, images)
    return redirect('units:units_list')
