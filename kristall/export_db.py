import csv
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kristall.settings')
django.setup()

from units.models import Buildings, Citys, Image, Published, Special, Streets, Unit

path = './data/'
os.mkdir(path)
os.chdir(path)

def write_city():
    citys = Citys.objects.all()
    print(citys)
    with open('city.csv', mode='a', encoding='utf-8') as csvfile:
        w_message = csv.writer(csvfile, delimiter=';', lineterminator='\r')
        for city in citys:
            w_message.writerow([city.pk, city.city])


def write_street():
    streets = Streets.objects.all()
    with open('street.csv', mode='a', encoding='utf-8') as csvfile:
        w_message = csv.writer(csvfile, delimiter=';', lineterminator='\r')
        for street in streets:
            w_message.writerow([street.pk, street.street])


def write_city():
    buildings = Buildings.objects.all()
    with open('building.csv', mode='a', encoding='utf-8') as csvfile:
        w_message = csv.writer(csvfile, delimiter=';', lineterminator='\r')
        for building in buildings:
            w_message.writerow(
                [building.pk, building.building, building.block, building.floors])


def write_unit():
    units = Unit.objects.all()
    with open('units.csv', mode='a', encoding='utf-8') as csvfile:
        w_message = csv.writer(csvfile, delimiter=';', lineterminator='\r')
        for unit in units:
            w_message.writerow(
                [unit.pk,
                 unit.name,
                 unit.author,
                 unit.square,
                 unit.description,
                 unit.city,
                 unit.street,
                 unit.build,
                 unit.floor,
                 unit.flat,
                 unit.price,
                 unit.deal])


def write_imgs():
    images = Image.objects.all()
    with open('img.csv', mode='a', encoding='utf-8') as csvfile:
        w_message = csv.writer(csvfile, delimiter=';', lineterminator='\r')
        for img in images:
            w_message.writerow(
                [img.pk,
                 img.unit,
                 img.image])


def write_publish():
    pub = Published.objects.all()
    with open('pub.csv', mode='a', encoding='utf-8') as csvfile:
        w_message = csv.writer(csvfile, delimiter=';', lineterminator='\r')
        for p in pub:
            w_message.writerow(
                [p.pk,
                 p.unit,
                 p.pub_date,
                 p.answer])


def write_special():
    spec = Special.objects.all()
    with open('spec.csv', mode='a', encoding='utf-8') as csvfile:
        w_message = csv.writer(csvfile, delimiter=';', lineterminator='\r')
        for p in spec:
            w_message.writerow(
                [p.pk,
                 p.unit,
                 p.pub_date,
                 p.answer])


if __name__ == '__main__':
    write_city()
    write_street()
    write_unit()
    write_imgs()
    write_publish()
    write_special()
    write_city()