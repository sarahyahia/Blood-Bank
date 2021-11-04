import random
from faker.providers import geo, BaseProvider
from django.core.management.base import BaseCommand
from faker import Faker
from city.models import City




    BLOOD_TYPES = [
        'A+', 'B+', 'A-', 'B-', 'AB+','AB-','O+', 'O-'
    ]
    
class Provider(BaseProvider):
    def blood_type(self):
        return self.random_element(BLOOD_TYPES)
    
    
class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):

        fake = Faker(["nl_NL"])
        
        for _ in range(100):
            City.objects.create(name=fake.city(), longitude=fake.longitude(), latitude= fake.latitude())
            
