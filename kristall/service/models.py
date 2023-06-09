from django.contrib.auth import get_user_model
from django.db import models
from units.models import Unit
from users.validators import PhoneValidator

User = get_user_model()


class Ip(models.Model):
    """Таблица всех IP адресов зашедших на сайт"""
    ip = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.ip}'


class Message(models.Model):
    message = models.TextField('Сообщение')
    name = models.CharField('ФИО', max_length=100)
    email = models.EmailField('E-mail', max_length=254, blank=True, null=True)
    phone = models.PositiveBigIntegerField(
        'Phone',
        validators=[PhoneValidator()]
    )
    date = models.DateField('Дата', auto_created=True, auto_now_add=True)
    ip = models.ForeignKey(
        Ip,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return f'{self.name}: {self.message}'[:100]

    def teleg_msg(self):
        if self.email:
            cnt = f'Контактные данные E-mail:{self.email}, Тел: {self.phone}'
        else:
            cnt = f'Контактные данные Тел: {self.phone}'
        return f'{self.name} оставил сообщение: {self.message}/{cnt}'


class UnitVisits(models.Model):
    """Связь с адресами просмотров объектов"""
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='visits'
    )
    views = models.ForeignKey(
        Ip,
        on_delete=models.CASCADE,
        related_name='unit_views',
        default=0
    )


class UserIp(models.Model):
    """Связь пользователя с адресами"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_ip')
    visits = models.ForeignKey(
        Ip,
        on_delete=models.CASCADE,
        related_name='user_visits',
        default=0
    )


class Post(models.Model):
    mark = models.SmallIntegerField(
        'Оценка',
        choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5),),
        default=5
    )
    text = models.TextField('Отзыв')
    author = models.CharField('Имя', max_length=20, default='Гость')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_created=True,
        auto_now=True
    )
    ip = models.ForeignKey(Ip, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_date']

    def stars(self):
        full_stars = ['1' * self.mark]
        empty_stars = ['0' * (5 - self.mark)]
        return list(full_stars[0]) + list(empty_stars[0])
