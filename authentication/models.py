from django.db import models
from django.contrib.auth.models import User
from city.models import City
from donor.models import *


class HospitalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=50, null=False, blank=False)
    
    class Meta:
        ordering = ("hospital_name",)
    
    def __str__(self):
        return str(self.hospital_name)



VIRUS_TEST_CHOICES=[
    ('Unknown', 'Unknown'),
    ('Positive', 'Positive'),
    ('Negative', 'Negative')
]


class DonorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=127)
    national_id = models.CharField(max_length=14,unique=True)
    city = models.ForeignKey(City ,on_delete=models.DO_NOTHING, null=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE)
    blood_virus_test = models.CharField(max_length=8,choices=VIRUS_TEST_CHOICES, default="Unknown")
    can_donate = models.BooleanField(default=False)
    last_donation_date = models.DateField(null=True ,blank=True)

    class Meta:
        ordering = ("name",'national_id',)
    
    def __str__(self):
        return str(self.national_id)