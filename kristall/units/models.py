from django.db import models


class Unit(models.Model):
    name = models.CharField('Название объекта', max_length=50)
    square = models.FloatField('Площадь')

    def __str__(self) -> str:
        description = '{}/{}'.format(self.name, self.square)
        return description

    def get_adress(self) -> str:
        return self.adress

    def is_published(self) -> bool:
        print(self.published)
        if self.published is None:
            return True
        return False


class Citys(models.Model):
    city = models.CharField('Город', max_length=25, default='Самара')


class Streets(models.Model):
    street = models.CharField('Улица', max_length=50)


class Buildings(models.Model):
    building = models.IntegerField('Здание')
    block = models.CharField('Корпус', max_length=5, blank=True, null=True)
    floors = models.IntegerField('Этажей в здании', blank=True, null=True)


class Flats(models.Model):
    floor = models.IntegerField('Этаж', blank=True, null=True)
    flat = models.IntegerField('Квартира', blank=True, null=True)


class Adress(models.Model):
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='adresses')
    city = models.ForeignKey(
        Citys, on_delete=models.CASCADE, related_name='adresses')
    street = models.ForeignKey(Streets, on_delete=models.CASCADE)
    building = models.ForeignKey(
        Buildings, on_delete=models.CASCADE, related_name='adresses')
    flat = models.ForeignKey(
        Flats, on_delete=models.CASCADE, related_name='adresses')

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Image(models.Model):
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='images')
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

    def __str__(self) -> str:
        if self.pub_date:
            return self.pub_date
        return False
