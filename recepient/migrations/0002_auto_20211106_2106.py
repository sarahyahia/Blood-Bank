# Generated by Django 3.2.9 on 2021-11-06 21:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('recepient', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ('-date',)},
        ),
        migrations.AddField(
            model_name='request',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
