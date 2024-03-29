from django.db import models
from city.models import City
from django.utils.timezone import now
import datetime
from django.core.validators import MaxValueValidator




class BloodType(models.Model):
    name = models.CharField(max_length=3)
    class Meta:
        ordering = ("name",)
    def __str__(self):
        return str(self.name)


VIRUS_TEST_CHOICES=[
    ('Unknown', 'Unknown'),
    ('Positive', 'Positive'),
    ('Negative', 'Negative')
]

class Donor(models.Model):
    name = models.CharField(max_length=127)
    email = models.EmailField(max_length=254,unique=True)
    national_id = models.CharField(max_length=14,unique=True)
    city = models.ForeignKey(City ,on_delete=models.DO_NOTHING, null=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE)
    blood_virus_test = models.CharField(max_length=8,choices=VIRUS_TEST_CHOICES, default="Unknown")
    can_donate = models.BooleanField(default=True)
    last_donation_date = models.DateField(null=True ,blank=True)

    class Meta:
        ordering = ("name",'national_id',)
    
    def __str__(self):
        return self.national_id


STATUS_CHOICES=[
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected')
]

class Donation(models.Model):
    donor = models.ForeignKey(to='authentication.DonorUser', on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(3)])
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)

    class Meta:
        ordering = ("donor",)
    
    def __str__(self):
        return self.donor.name

class BloodStock(models.Model):
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE)
    blood_bank_city = models.ForeignKey(City ,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(3)])
    expiration_date = models.DateField(default=now()+datetime.timedelta(days=42))
    
    class Meta:
        ordering = ("-expiration_date",)
    
    def __str__(self):
        return str(self.blood_type)