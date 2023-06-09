import csv
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kristall.settings')
django.setup()

from units.models import (
    Buildings, Citys, Image, Published, Special, Streets, Unit, User
)
path = './data/'
os.chdir(path)

def write_city():
    citys = Citys.objects.all()
    citys.delete()
    with open('city.csv', mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['pk', 'city'], delimiter=';')
        citys = (Citys(pk=_['pk'], city=_['city']) for _ in reader)
        Citys.objects.bulk_create(citys)
        csvfile.close()


def write_street():
    streets = Streets.objects.all()
    streets.delete()
    with open('street.csv', mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['pk', 'street'], delimiter=';')
        streets = (Streets(pk=_['pk'], street=_['street']) for _ in reader)
        Streets.objects.bulk_create(streets)
        csvfile.close()


def write_building():
    buildings = Buildings.objects.all()
    buildings.delete()
    with open('building.csv', mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(
            csvfile,
            fieldnames=['pk', 'building', 'block', 'floors'],
            delimiter=';'
        )
        buildings = (Buildings(
            pk=_['pk'],
            building=_['building'],
            block=_['block'],
            floors=_['floors'] if _['floors'] else None
        ) for _ in reader)
        Buildings.objects.bulk_create(buildings)
        csvfile.close()


def write_unit():
    units = Unit.objects.all()
    units.delete()
    with open('units.csv', mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=[
            'pk',
            'name',
            'author',
            'square',
            'description',
            'city',
            'street',
            'build',
            'floor',
            'flat',
            'price',
            'deal'],
            delimiter=';')
        units = (Unit(
            pk=_['pk'],
            name=_['name'],
            author= User.objects.get(pk=_['author']),
            square=_['square'],
            description=_['description'],
            city=Citys.objects.get(pk=_['city']),
            street=Streets.objects.get(id=_['street']),
            build=Buildings.objects.get(id=_['build']),
            floor=(_['floor'] if _['floor'] else None),
            flat=(_['flat'] if _['flat'] else None),
            price=_['price'],
            deal=_['deal']
        ) for _ in reader)
        Unit.objects.bulk_create(units)
    csvfile.close()


def write_imgs():
    images = Image.objects.all()
    images.delete()
    with open('img.csv', mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['pk', 'unit', 'image'], delimiter=';')
        imgs = (Image(
            pk=_['pk'],
            unit=Unit.objects.get(id=_['unit']),
            image=_['image']
        ) for _ in reader)
        Image.objects.bulk_create(imgs)
        csvfile.close()


def write_publish():
    pub = Published.objects.all()
    pub.delete()
    with open('pub.csv', mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', fieldnames=[
            'pk',
            'unit',
            'pub_date',
            'answer'
        ])
        pub = (Published(
            pk=_['pk'],
            unit=Unit.objects.get(id=_['unit']),
            pub_date=_['pub_date'],
            answer=_['answer']
         ) for _ in reader)
        Published.objects.bulk_create(pub)
    csvfile.close()


def write_special():
    spec = Special.objects.all()
    spec.delete()
    with open('spec.csv', mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', fieldnames=[
            'pk',
            'unit',
            'pub_date',
            'answer'])
        sp = (Special(
            pk=_['pk'],
            unit=Unit.objects.get(id=_['unit']),
            pub_date=_['pub_date'],
            answer=_['answer']
        ) for _ in reader)
        Special.objects.bulk_create(sp)
    csvfile.close()


if __name__ == '__main__':
    write_city()
    write_street()
    write_building()
    write_unit()
    write_imgs()
    write_publish()
    write_special()
    
