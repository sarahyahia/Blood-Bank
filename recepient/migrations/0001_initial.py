# Generated by Django 3.2.9 on 2021-11-06 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('donor', '0017_auto_20211106_2030'),
        ('authentication', '0003_rename_hopitaluser_hospitaluser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_status', models.CharField(choices=[('Immediate', 'Immediate'), ('Urgent', 'Urgent'), ('Normal', 'Normal')], max_length=9)),
                ('request_status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=8)),
                ('quantity', models.IntegerField()),
                ('blood_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donor.bloodtype')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.hospitaluser')),
            ],
        ),
    ]
