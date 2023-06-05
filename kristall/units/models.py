from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

User = get_user_model()

SALE = 'Продажа'
RENT = 'Аренда'

deals = [
    (SALE, SALE),
    (RENT, RENT),
]


class Citys(models.Model):
    """Model City for adress"""
    city = models.CharField('Город', max_length=25, default='Самара')

    def __str__(self) -> str:
        return str(self.city)


class Streets(models.Model):
    """Street objects for adress"""
    street = models.CharField('Улица', max_length=50)

    def __str__(self) -> str:
        return str(self.street)


class Buildings(models.Model):
    """Home params"""
    building = models.IntegerField('Дом.')
    block = models.CharField('Корпус', max_length=5, blank=True, null=True)
    floors = models.IntegerField('Этажность здания', blank=True, null=True)

    def __str__(self) -> str:
        if self.block:
            return f'дом № {self.building}, корп. {self.block}'
        return f'дом № {self.building}'


class Unit(models.Model):
    """Unit params"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='units',
        verbose_name='Автор'
    )
    name = models.CharField('Название объекта', max_length=50)
    square = models.FloatField('Площадь, m2')
    description = models.TextField('Описание объекта', blank=True, null=True)
    city = models.ForeignKey(
        Citys, on_delete=models.CASCADE, related_name='units')
    street = models.ForeignKey(
        Streets, on_delete=models.CASCADE, related_name='units')
    build = models.ForeignKey(
        Buildings, on_delete=models.CASCADE, related_name='units')
    floor = models.IntegerField('Этаж', blank=True, null=True)
    flat = models.IntegerField('Номер помещения', blank=True, null=True)
    price = models.FloatField('Цена, руб', max_length=2)
    deal = models.CharField(
        'Тип предложения',
        choices=deals,
        max_length=max(len(deal[1]) for deal in deals), default=SALE
    )

    class Meta:
        ordering = ['-pk']

    def __str__(self) -> str:
        if str(self.name)[-1] not in ['.', ',', '!', ';', ':']:
            return f'{self.name}, {self.square}'.upper()
        return f'{self.name} {self.square}'.upper()

    def adress(self) -> str:
        return f'г. {self.city}, ул. {self.street}, {self.build}'

    def is_published(self) -> bool:
        if len(self.published.all()) > 0:
            return self.published.all()[0].pub_date
        return False

    def is_special(self) -> bool:
        if len(self.special.all()) > 0:
            return self.special.all()[0].pub_date
        return False

    def main_image(self):
        if len(self.images.all()) > 0:
            return self.images.all()[0].image
        return None

    def get_images(self):
        return self.images.all()

    def get_image_filename(self, filename):
        title = self.unit.title
        slug = slugify(title)
        return 'unit_images/%s-%s' % (slug, filename)

    def price_per_metr(self) -> float:
        return '{:,}'.format(
            int(self.price / self.square)).replace(',', '`')

    def unit_price(self):
        return '{:,}'.format(int(self.price)).replace(',', '`')

    def get_short_description(self):
        return self.description[:200]

    def check_param(self, param_min, param, param_max):
        return param_min <= param <= param_max


class Image(models.Model):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        default=None,
        related_name='images')
    image = models.ImageField(
        'Фотография',
        upload_to='units/',
        blank=True,
        null=True
    )


class Published(models.Model):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='published'
    )
    pub_date = models.DateTimeField(
        'Время размещения',
        auto_created=True)
    answer = models.BooleanField(
        default=True
    )

    def __str__(self) -> str:
        if self.pub_date:
            return str('True')
        return False


class Special(models.Model):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='special'
    )
    pub_date = models.DateTimeField(
        'Время размещения',
        auto_created=True)
    answer = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Специальное предложение'

    def __str__(self) -> str:
        if self.pub_date:
            return str('True')
        return False
