# Generated by Django 3.2.9 on 2021-11-13 17:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0024_auto_20211113_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodstock',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 25, 17, 9, 59, 676015, tzinfo=utc)),
        ),
    ]
