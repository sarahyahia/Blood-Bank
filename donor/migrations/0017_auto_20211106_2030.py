# Generated by Django 3.2.9 on 2021-11-06 20:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0016_auto_20211104_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodstock',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 18, 20, 30, 37, 43264, tzinfo=utc)),
        ),
    ]
