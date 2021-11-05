from django import forms
from .models import Donor, BloodType, Donation
from city.models import City
import datetime



class DonorForm(forms.ModelForm):
    national_id = forms.CharField(label="National ID",help_text='exact 14 unique number.')
    city = forms.ModelChoiceField(label=('city'),queryset=City.objects.all())
    blood_type = forms.ModelChoiceField(label=('Blood Type'),queryset=BloodType.objects.all())
    
    class Meta:
        model = Donor
        fields = ['name', 'email','city', 'national_id', 'blood_type','last_donation_date']
        widgets= {
            'last_donation_date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select Date','type': 'date'})
        }



class DonationForm(forms.ModelForm):
    donor = forms.ModelChoiceField(label=('Donor'),queryset=Donor.objects.all())
    class Meta:
        model = Donation
        fields = ['donor', 'quantity']