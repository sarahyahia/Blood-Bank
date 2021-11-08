import random
from faker.providers import geo, BaseProvider
from django.core.management.base import BaseCommand
from faker import Faker
from city.models import City
from donor.models import Donor, BloodType, Donation, BloodStock
from faker.providers import DynamicProvider
import datetime


site_city_provider = DynamicProvider(
    provider_name="site_city",
    elements=list(City.objects.all()),
)
    
class Provider(BaseProvider):
    def blood_type(self):
        return self.random_element(list(BloodType.objects.all()))
    def blood_virus_test(self):
        return self.random_element(['Unknown', 'Positive', 'Negative'])
    def donor(self):
        return self.random_element(list(Donor.objects.all()))
    
class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):

        fake = Faker(["nl_NL"])
        fake.add_provider(Provider)
        fake.add_provider(site_city_provider)
        
        
        
        for _ in range(100):
            # City.objects.create(name=fake.city(), longitude=fake.longitude(), latitude= fake.latitude())
            # name = fake.name()
            # national_id = random.randint(23001010000000,32111089999999)
            # email = fake.unique.email()
            # Donor.objects.create(
            #     national_id=national_id,
            #     email=email,
            #     name=name,
            #     city=fake.site_city(),
            #     blood_type=fake.blood_type(),
            #     blood_virus_test=fake.blood_virus_test(),
            #     can_donate=False,
            #     last_donation_date=fake.past_date()
            # )
            # Donation.objects.create(
            #     donor = fake.donor(),
            #     quantity = random.randint(1,3),
            #     status = 'pending'
            # )
            
            BloodStock.objects.create(
                blood_type= fake.blood_type(),
                blood_bank_city = fake.site_city(),
                quantity = random.randint(1,3),
                expiration_date = fake.past_date()+datetime.timedelta(days=42)
            )
