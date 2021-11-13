from django import forms
from allauth.account.forms import LoginForm, SignupForm
from .models import HospitalUser, DonorUser
from city.models import City
from donor.models import BloodType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



def validate_national_id(value):
    if len(value)!=14 or not value.isdecimal():
        raise ValidationError(
            _('%(value)s is not a valid national ID'),
            params={'value': value},
        )
    elif DonorUser.objects.filter(national_id=value).exists():
        raise ValidationError(
            _('%(value)s is already registered'),
            params={'value': value},
        )




class HospitalSignupForm(SignupForm):
    city = forms.ModelChoiceField(label=('City'),queryset=City.objects.all())
    hospital_name = forms.CharField(label=('Hospital Name'),max_length=50, required=True, strip=True)

    def save(self, request):
        user = super(HospitalSignupForm, self).save(request)
        hospital_user = HospitalUser(
            user=user,
            city=self.cleaned_data.get('city'),
            hospital_name=self.cleaned_data.get('hospital_name')
        )
        hospital_user.save()
        return hospital_user.user



class DonorSignupForm(SignupForm):
    name = forms.CharField(label=('Name'),max_length=50, required=True, strip=True)
    national_id = forms.CharField(label="National ID",help_text='exact 14 unique number.', validators=[validate_national_id])
    city = forms.ModelChoiceField(label=('City'),queryset=City.objects.all())
    blood_type = forms.ModelChoiceField(label=('Blood Type'),queryset=BloodType.objects.all())
    last_donation_date = forms.DateField(label="Last donation date",widget = forms.DateInput(attrs={'class': 'datepicker'}), required=False)

    def save(self, request):
        user = super(DonorSignupForm, self).save(request)
        donor_user = DonorUser(
            user=user,
            name=self.cleaned_data.get('name'),
            national_id=self.cleaned_data.get('national_id'),
            city = self.cleaned_data.get('city'),
            blood_type = self.cleaned_data.get('blood_type'),
            last_donation_date = self.cleaned_data.get('last_donation_date'),
        )
        donor_user.save()
        return donor_user.user