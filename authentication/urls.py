from django.urls import path
from .views import HospitalSignupView


urlpatterns = [
    path('signup/', HospitalSignupView.as_view(), name='hospital-signup'),
]