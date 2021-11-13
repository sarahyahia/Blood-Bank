from django import forms
from .models import Donor, BloodType, Donation
from city.models import City
import datetime


class DonationForm(forms.ModelForm):
    donor = forms.ModelChoiceField(label=('Donor'),queryset=Donor.objects.all())
    class Meta:
        model = Donation
        fields = ['donor', 'quantity']