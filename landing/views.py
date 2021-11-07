from django.shortcuts import render
from django.views import View
from helpers.decorators import auth_user_should_not_access

@auth_user_should_not_access
def index(request):
    return render(request, 'landing/index.html')