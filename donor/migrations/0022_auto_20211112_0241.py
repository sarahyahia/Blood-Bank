# Generated by Django 3.2.9 on 2021-11-12 02:41

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_donoruser_can_donate'),
        ('donor', '0021_auto_20211111_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodstock',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 24, 2, 41, 40, 547681, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='donation',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='authentication.donoruser'),
        ),
    ]
