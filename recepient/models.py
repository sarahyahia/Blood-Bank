from django.db import models
from django.contrib.auth.models import User
from donor.models import BloodType
from authentication.models import HospitalUser





PATIENT_STATUS_CHOICES=[
    ('Immediate', 'Immediate'),
    ('Urgent', 'Urgent'),
    ('Normal', 'Normal')
]

STATUS_CHOICES=[
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected')
]

class Request(models.Model):
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE)
    patient_status = models.CharField(max_length=9,choices=PATIENT_STATUS_CHOICES)
    request_status = models.CharField(max_length=8,choices=STATUS_CHOICES)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date",)
    
    def __str__(self):
        return self.date


# class Notification(models.Model):
#     body = models.TextField(max_length=255)
#     reciever = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     recieved_date = models.DateTimeField(auto_now_add=True)