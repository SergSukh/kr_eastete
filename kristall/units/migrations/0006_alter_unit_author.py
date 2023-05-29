# Generated by Django 4.2 on 2023-05-24 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('units', '0005_message_phone_alter_message_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]