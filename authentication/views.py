from django.shortcuts import render
from allauth.account.views import SignupView
from .forms import HospitalSignupForm
from helpers.decorators import auth_user_should_not_access, NotAuthenticatedMixin



# @auth_user_should_not_access
class HospitalSignupView(NotAuthenticatedMixin,SignupView):
    
    form_class = HospitalSignupForm

#     # success_url = None
    redirect_field_name = 'requests'

