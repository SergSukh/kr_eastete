import telegram
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect, render

from .models import Ip, Message, Unit, UnitVisits, UnitLocation, UserIp

bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)


def get_client_ip(request):
    x_frwrdd = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_frwrdd:
        return x_frwrdd.split(',')[0]
    return (
        f"{request.META.get('REMOTE_ADDR')}: {request.META.get('REMOTE_PORT')}"
    )


def save_ip(request):
    ip = get_client_ip(request)
    if not Ip.objects.filter(ip=ip).exists():
        Ip.objects.create(ip=ip)
    return Ip.objects.get(ip=ip)


def msg_create(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    msg = request.POST.get('message')
    ip = Ip.objects.get_or_create(ip=get_client_ip(request))
    text = Message.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=msg,
        ip=ip[0]
    )
    bot.send_message(chat_id=settings.TELEGRAM_CHAT, text=text.teleg_msg())
    return redirect('units:units_list')


def save_user_ip(request):
    if request.user.is_authenticated:
        user = request.user
        ip = save_ip(request)
        if not user.user_ip.filter(visits=ip).exists():
            UserIp.objects.create(user=user, visits=ip)


def save_unit_ip(request, unit):
    ip = save_ip(request)
    if not unit.visits.filter(views=ip).exists():
        UnitVisits.objects.create(unit=unit, views=ip)


def get_unit_geocode(unit):
    return UnitLocation.objects.get_or_create(unit=unit)[0]

def get_search_min_param(param):
    return (float(param) if param else 0)


def get_search_max_param(param):
    return (float(param) if param else 999999999)


def get_list_find_units(request):
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
    return obj_list


def map_units_search(request):
    objs = get_list_find_units(request)
    for obj in objs:
        objs.coord = get_unit_geocode(obj)

    return render(request, 'maps/search_units.html', {'objs': objs})