# Generated by Django 4.2 on 2023-04-29 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0002_alter_adress_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='is_published',
        ),
    ]
