from django.db import models
from django.contrib.auth.models import User
from donor.models import BloodType
from authentication.models import HospitalUser
from city.models import City




PATIENT_STATUS_CHOICES=[
    (1, 'Immediate'),
    (2, 'Urgent'),
    (3, 'Normal')
]

STATUS_CHOICES=[
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected')
]

class Request(models.Model):
    hospital = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
    blood_type = models.ForeignKey(BloodType, on_delete=models.CASCADE)
    patient_status = models.IntegerField(choices=PATIENT_STATUS_CHOICES)
    request_status = models.CharField(max_length=8,choices=STATUS_CHOICES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date",)
    
    def __str__(self):
        return str(self.id)



# class BloodTransaction(models.Model):
#     request = models.ForeignKey(Request, related_name='AcceptedRequest', on_delete=models.DO_NOTHING)
#     date = models.DateTimeField(auto_now_add=True)
#     blood_bank_city = models.ForeignKey(City, related_name='BloodBank', on_delete=models.DO_NOTHING)

#     class Meta:
#         ordering = ("-date",)
    
#     def __str__(self):
#         return self.blood_bank_city

# class Notification(models.Model):
#     body = models.TextField(max_length=255)
#     reciever = models.ForeignKey(HospitalUser, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     recieved_date = models.DateTimeField(auto_now_add=True)