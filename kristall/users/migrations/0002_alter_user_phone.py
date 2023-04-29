# Generated by Django 4.2 on 2023-04-29 07:31

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(blank=True, null=True, validators=[users.validators.PhoneValidator()], verbose_name='Phone'),
        ),
    ]
