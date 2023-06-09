# Generated by Django 4.2 on 2023-07-07 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buildings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.IntegerField(verbose_name='Дом.')),
                ('block', models.CharField(blank=True, max_length=5, null=True, verbose_name='Корпус')),
                ('floors', models.IntegerField(blank=True, null=True, verbose_name='Этажность здания')),
            ],
        ),
        migrations.CreateModel(
            name='Citys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='Самара', max_length=50, verbose_name='Город')),
            ],
        ),
        migrations.CreateModel(
            name='Streets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=75, verbose_name='Улица')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название объекта')),
                ('square', models.FloatField(verbose_name='Площадь, m2')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание объекта')),
                ('floor', models.IntegerField(blank=True, null=True, verbose_name='Этаж')),
                ('flat', models.IntegerField(blank=True, null=True, verbose_name='Номер помещения')),
                ('price', models.FloatField(max_length=2, verbose_name='Цена, руб')),
                ('deal', models.CharField(choices=[('Продажа', 'Продажа'), ('Аренда', 'Аренда')], default='Продажа', max_length=7, verbose_name='Тип предложения')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('build', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='units.buildings')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='units.citys')),
                ('street', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='units.streets')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_created=True, verbose_name='Время размещения')),
                ('answer', models.BooleanField(default=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special', to='units.unit')),
            ],
            options={
                'verbose_name': 'Специальное предложение',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Published',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_created=True, verbose_name='Время размещения')),
                ('answer', models.BooleanField(default=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='published', to='units.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='units/', verbose_name='Фотография')),
                ('unit', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='units.unit')),
            ],
        ),
    ]
