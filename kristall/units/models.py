from django.db import models


class Unit(models.Model):
    name = models.CharField('Название объекта', max_length=50)
    square = models.FloatField('Площадь')
    published = models.BooleanField('Опубликовано', default=False)


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


class Image(models.Model):
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        'Фотография',
        upload_to='units/',
        blank=True,
        null=True
    )
