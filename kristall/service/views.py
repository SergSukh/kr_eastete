from datetime import datetime as dt

import telegram
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .forms import PostForm
from .models import Ip, Message, Post, UnitVisits, UserIp

bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)


def pages(request, unit_list):
    units_in_page = settings.UNITS_IN_PAGE
    paginator = Paginator(unit_list, units_in_page)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)


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
        Ip.objects.create(ip=ip, description=str(request.META))
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


def feedback(request):
    post_objects = Post.objects.all()
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = (
            form.cleaned_data['author'] if form['author'] else 'Гость'
        )
        post.pub_date = dt.now()
        post.ip = save_ip(request)
        post.save()
        return render(request, 'units/index.html')
    context = {
        'page_obj': pages(request, post_objects),
        'form': form
    }
    return render(request, 'service/feedback.html', context)
