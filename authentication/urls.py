from django.urls import path
from .views import HospitalSignupView, DonorSignupView, signup_choices, profile


urlpatterns = [
    path('signup/', signup_choices, name='signup-choices' ),
    path('donor/signup/', DonorSignupView.as_view(), name='donor-signup'),
    path('hospital/signup/', HospitalSignupView.as_view(), name='hospital-signup'),
    path('profile/', profile, name='profile'),
]