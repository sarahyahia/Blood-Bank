from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from validate_email import validate_email
from .models import Donor, BloodType, Donation
from django.core.paginator import Paginator
from .forms import DonorForm
from city.models import City
from django.urls import reverse
from django.contrib import messages
from datetime import datetime, date
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse


def days_between(d):
    d1 = datetime.strptime(d, "%Y-%m-%d")
    d2 = datetime.strptime(str(date.today()), "%Y-%m-%d")
    diff = (d2 - d1).days
    return diff


########################################################

def validate_national_id(value,request):
    if len(value)!=14 or not value.isdecimal():
        messages.add_message(request, messages.ERROR, 'The National ID must be 14 numbers')
        return False
    elif Donor.objects.filter(national_id=value).exists():
        messages.add_message(request, messages.ERROR, f'{value} is already registered')
        return False
    return True


########################################################

def index(request):
    donors = Donor.objects.all()
    paginator = Paginator(donors, 5)
    pg_number = request.GET.get('page')
    pg_object = Paginator.get_page(paginator,pg_number)
    context = {
        'donors':donors,
        "pg_object":pg_object,
    }
    return render(request, 'donor/home.html',context)


########################################################

def donor_details(request,id):
    donor = get_object_or_404(Donor, pk=id)
    context = {
        'donor':donor,
    }
    return render(request, 'donor/donor_details.html',context)


########################################################

def add_donor(request):
    form = DonorForm()
    context = {'form': form}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        national_id  = request.POST.get('national_id')
        cityinstance         = request.POST.get('city')
        blood_typeinstance   = request.POST.get('blood_type')
        last_donation_date = request.POST.get('last_donation_date')
        
        if not validate_national_id(national_id, request):
            return render(request, 'donor/add_donor.html',context)
        
        if not validate_email(email):
            messages.add_message(request, messages.ERROR,'Enter a valid email address')
            return render(request, 'donor/add_donor.html',context)
        elif Donor.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,'This Email is already in use')
            return render(request, 'donor/add_donor.html',context)
        
        if last_donation_date :
            diff_days = days_between(last_donation_date)
            if diff_days<0 :
                messages.add_message(request,messages.ERROR, 'The Last Donation Date must be in the past!')
                return render(request, 'donor/add_donor.html',context)
            elif diff_days/30 < 3: 
                donor.can_donate = False
                # ************
            donor.last_donation_date = last_donation_date
        
        blood_type = BloodType.objects.get(pk=blood_typeinstance)
        city = City.objects.get(pk=cityinstance)
        donor = Donor()
        donor.name = name
        donor.email = email
        donor.city = city 
        donor.blood_type = blood_type  
        donor.national_id = national_id
        
        donor.save()
        messages.add_message(request, messages.SUCCESS, 'donor was added successfully')
        return HttpResponseRedirect(reverse("donor", kwargs={'id': donor.pk}))  # reverse because we don't know the id
    return render(request, 'donor/add_donor.html',context)


########################################################

def edit_donor(request,id):
    donor = get_object_or_404(Donor, pk=id)
    cities = City.objects.all()
    blood_types = BloodType.objects.all()
    context = {
        'donor':donor,
        'cities':cities,
        'blood_types':blood_types,
    }
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        national_id  = request.POST.get('national_id')
        last_donation_date = request.POST.get('last_donation_date')
        cityinstance         = request.POST.get('city')
        blood_typeinstance   = request.POST.get('blood_type')
        blood_virus_test = request.POST.get('blood_virus_test')
        
        
        
        if len(national_id)!=14 or not national_id.isdecimal():
            messages.add_message(request, messages.ERROR, 'The National ID must be 14 numbers')
            return render(request, 'donor/edit_donor.html',context)
        elif Donor.objects.filter(national_id=national_id).exists() and donor.national_id!=national_id :
            messages.add_message(request, messages.ERROR, f'{value} is already registered')
            return render(request, 'donor/edit_donor.html',context)
        
        if not validate_email(email):
            messages.add_message(request, messages.ERROR,'Enter a valid email address')
            return render(request, 'donor/add_donor.html',context)
        elif Donor.objects.filter(email=email).exists() and donor.email!=email :
            messages.add_message(request, messages.ERROR,'This Email is already in use')
            return render(request, 'donor/add_donor.html',context)
        
        if last_donation_date :
            diff_days = days_between(last_donation_date)
            if diff_days<0 :
                messages.add_message(request,messages.ERROR, 'The Last Donation Date must be in the past!')
                return render(request, 'donor/edit_donor.html',context)
            elif diff_days/30 < 3: 
                donor.can_donate = False
                # ************
            donor.last_donation_date = datetime.strptime(last_donation_date, "%Y-%m-%d")
        
        
        if blood_virus_test:
            pass # send email to the donor    
        
        
        blood_type = BloodType.objects.get(pk=blood_typeinstance)
        city = City.objects.get(pk=cityinstance)
        
        donor.name = name
        donor.email = email
        donor.city = city 
        donor.national_id = national_id
        donor.blood_type  = blood_type  
        donor.blood_virus_test = blood_virus_test
        
        donor.save()
        messages.add_message(request, messages.SUCCESS, 'donor was edited successfully')
        return HttpResponseRedirect(reverse("donor", kwargs={'id': donor.pk}))  # reverse because we don't know the id
    
    return render(request, 'donor/edit_donor.html',context)


########################################################

def delete_donor(request, id):
    donor = get_object_or_404(Donor, pk=id)
    context = {'donor':donor}
    if request.method == 'POST':
        donor.delete()
        messages.add_message(request, messages.SUCCESS, 'Donor was deleted successfully')
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'donor/delete_donor.html', context)


########################################################

def search_donors(request):
    if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            donors = Donor.objects.filter(national_id__startswith= search_str 
                        ) | Donor.objects.filter(
                        city__name__istartswith=search_str )
            donor_list = []
            for donor in donors:
                donor_list.append({
                "id": donor.id,
                "name": donor.name,
                "national_id": donor.national_id,
                "city": donor.city.name,
                "blood_type": donor.blood_type.name,
                })
            return JsonResponse(donor_list, safe=False) # safe parameter for parsing list {not object} data without problems


########################################################


def donation_list(request):
    donation_list = Donation.objects.all()
    context = {
        'donations':donation_list,
    }
    return render(request, 'donation/donation_list.html')