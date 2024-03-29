# Generated by Django 3.2.9 on 2021-11-04 15:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0009_auto_20211104_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodstock',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 16, 15, 1, 43, 6643, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='donor',
            name='blood_virus_test',
            field=models.BooleanField(null=True),
        ),
    ]
