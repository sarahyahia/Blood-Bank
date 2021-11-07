from django import forms
from allauth.account.forms import LoginForm, SignupForm
from .models import HospitalUser
from city.models import City


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
