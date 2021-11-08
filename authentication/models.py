from django.db import models
from django.contrib.auth.models import User
from city.models import City


class HospitalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=50, null=False, blank=False)
    
    class Meta:
        ordering = ("hospital_name",)
    
    def __str__(self):
        return str(self.hospital_name)