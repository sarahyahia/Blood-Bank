# Generated by Django 3.2.9 on 2021-11-04 22:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0015_auto_20211104_2136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bloodstock',
            options={'ordering': ('blood_type',)},
        ),
        migrations.AlterField(
            model_name='bloodstock',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 16, 22, 54, 11, 511692, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='donor',
            name='can_donate',
            field=models.BooleanField(default=True),
        ),
    ]
