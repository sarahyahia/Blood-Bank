# Generated by Django 3.2.9 on 2021-11-03 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0004_remove_donor_blood_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='blood_type',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='donor.bloodtype'),
            preserve_default=False,
        ),
    ]