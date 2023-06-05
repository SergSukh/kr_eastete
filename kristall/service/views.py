import telegram
from django.conf import settings
from django.shortcuts import redirect

from .models import Ip, Message, UnitVisits, UserIp

bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)


def get_client_ip(request):
    x_frwrdd = request.META.get('HTTP_X_FORWARDED_FOR')
    print(request.META)
    if x_frwrdd:
        return x_frwrdd.split(',')[0]
    return request.META.get('REMOTE_ADDR')


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
