from django.shortcuts import render
from .models import HospitalUser, DonorUser
from allauth.account.views import SignupView
from .forms import HospitalSignupForm, DonorSignupForm
from helpers.decorators import auth_user_should_not_access, NotAuthenticatedMixin




def who(request):
    hospital = None
    donor = None
    is_admin = False
    try:
        donor = DonorUser.objects.get(user=request.user)
    except DonorUser.DoesNotExist:
        donor = None
        try:
            hospital = HospitalUser.objects.get(user=request.user)
        except HospitalUser.DoesNotExist:
            hospital = None
            is_admin = True
    context = {
        'donor': donor,
        'hospital':hospital,
        'is_admin': is_admin,
    }
    return context




class HospitalSignupView(NotAuthenticatedMixin,SignupView):
    
    form_class = HospitalSignupForm
    template_name = 'account/signup_hospital.html'

#     # success_url = None
    redirect_field_name = 'profile'

class DonorSignupView(NotAuthenticatedMixin,SignupView):
    
    form_class = DonorSignupForm

#     # success_url = None
    redirect_field_name = 'profile'


def signup_choices(request):
    return render(request, 'authentication/signup_choices.html')


def profile(request):
    context = who(request)
    return render(request, 'authentication/profile.html', context)