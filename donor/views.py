from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from validate_email import validate_email
from .models import Donor, BloodType, Donation, BloodStock
from authentication.models import DonorUser
from django.core.paginator import Paginator
from .forms import DonationForm
from city.models import City
from django.urls import reverse
from django.contrib import messages
from datetime import datetime, date
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.timezone import datetime
import threading
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from helpers.decorators import staff_required
from django.db.models.functions import Now
from authentication.views import who


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


########################################################



def send_rejection_email(donor, diff_months = None):
    htmly = get_template('donation/Email.html')
    context = {
        'donor':donor,
        'diff_months': int(diff_months),
    }
    subject, from_email,to = 'Blood Donation Response', settings.EMAIL_HOST_USER, donor.user.email
    html_content = htmly.render(context)
    email = EmailMultiAlternatives(subject, html_content, from_email, [to])
    email.attach_alternative(html_content, "text/html")

    if not settings.TESTING:
        EmailThread(email).start()


########################################################


def days_between(d):
    d1 = datetime.strptime(d, "%Y-%m-%d")
    d2 = datetime.strptime(str(date.today()), "%Y-%m-%d")
    diff = (d2 - d1).days
    return diff




########################################################


def get_showing_donors(request):
    print('enter')
    if request.GET and request.GET.get('filter'):
        print(request.GET.get('filter'))
        if request.GET.get('filter') == 'unknown':
            donors = DonorUser.objects.filter(blood_virus_test="Unknown")
        elif request.GET.get('filter') == 'positive':
            donors = DonorUser.objects.filter(blood_virus_test= 'Positive')
        elif request.GET.get('filter') == 'Negative':
            donors = DonorUser.objects.filter(blood_virus_test= 'Negative')
        else:
            donors = DonorUser.objects.all()
        return donors


########################################################

@staff_required(login_url='/')
def index(request):
    donors = DonorUser.objects.all()
    # donors_list = get_showing_donors(request)
    unknown = DonorUser.objects.filter(blood_virus_test="Unknown").count
    positive = DonorUser.objects.filter(blood_virus_test= 'Positive').count
    negative = DonorUser.objects.filter(blood_virus_test= 'Negative').count
    paginator = Paginator(donors, 20)
    pg_number = request.GET.get('page')
    pg_object = Paginator.get_page(paginator,pg_number)
    context = {
        'donors': donors,
        'all_count': donors.count,
        'unknown':unknown,
        'positive':positive,
        'negative':negative,
        "pg_object":pg_object,
    }
    return render(request, 'donor/home.html',context)


########################################################
@staff_required(login_url='/')
def donor_details(request,id):
    donor = get_object_or_404(DonorUser, pk=id)
    context = {
        'donor':donor,
    }
    return render(request, 'donor/donor_details.html',context)


########################################################
# @staff_required(login_url='/')
# def add_donor(request):
#     form = DonorForm()
#     context = {'form': form}
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         national_id  = request.POST.get('national_id')
#         cityinstance         = request.POST.get('city')
#         blood_typeinstance   = request.POST.get('blood_type')
#         last_donation_date = request.POST.get('last_donation_date')
        
#         if not validate_national_id(national_id, request):
#             return render(request, 'donor/add_donor.html',context)
        
#         if not validate_email(email):
#             messages.add_message(request, messages.ERROR,'Enter a valid email address')
#             return render(request, 'donor/add_donor.html',context)
#         elif Donor.objects.filter(email=email).exists():
#             messages.add_message(request, messages.ERROR,'This Email is already in use')
#             return render(request, 'donor/add_donor.html',context)
        
#         donor = Donor()
        
#         if last_donation_date :
#             diff_days = days_between(last_donation_date)
#             if diff_days<0 :
#                 messages.add_message(request,messages.ERROR, 'The Last Donation Date must be in the past!')
#                 return render(request, 'donor/add_donor.html',context)
#             elif diff_days/30 < 3: 
#                 donor.can_donate = False
#                 # ************
#             donor.last_donation_date = last_donation_date
        
#         blood_type = BloodType.objects.get(pk=blood_typeinstance)
#         city = City.objects.get(pk=cityinstance)
#         donor.name = name
#         donor.email = email
#         donor.city = city 
#         donor.blood_type = blood_type  
#         donor.national_id = national_id
        
#         donor.save()
#         messages.add_message(request, messages.SUCCESS, 'donor was added successfully')
#         return HttpResponseRedirect(reverse("donor", kwargs={'id': donor.pk}))  # reverse because we don't know the id
#     return render(request, 'donor/add_donor.html',context)


########################################################

@staff_required(login_url='/')
def edit_donor(request,id):
    donor = get_object_or_404(DonorUser, pk=id)
    cities = City.objects.all()
    blood_types = BloodType.objects.all()
    context = {
        'donor':donor,
        'cities':cities,
        'blood_types':blood_types,
    }
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        last_donation_date = request.POST.get('last_donation_date')
        cityinstance         = request.POST.get('city')
        blood_typeinstance   = request.POST.get('blood_type')
        blood_virus_test = request.POST.get('blood_virus_test')
        
        if last_donation_date :
            print(last_donation_date)
            diff_days = days_between(last_donation_date)
            if diff_days<0 :
                messages.add_message(request,messages.ERROR, 'The Last Donation Date must be in the past!')
                return render(request, 'donor/edit_donor.html',context)
            elif diff_days/30 < 3: 
                print(donor.can_donate)
                donor.can_donate = False
                send_rejection_email(donor, diff_days/30)
                # ************
            elif diff_days/30 >3: 
                donor.can_donate = True
            donor.last_donation_date = datetime.strptime(last_donation_date, "%Y-%m-%d")
        elif not donor.last_donation_date:
            donor.can_donate = True
                
        blood_type = BloodType.objects.get(pk=blood_typeinstance)
        city = City.objects.get(pk=cityinstance)
        
        donor.name = name
        donor.city = city
        donor.blood_type  = blood_type  
        
        if blood_virus_test:
            donor.blood_virus_test = blood_virus_test
        
        donor.save()
        messages.add_message(request, messages.SUCCESS, 'donor was edited successfully')
        
        donations = Donation.objects.filter(donor = donor)
        for donation in donations:
            if blood_virus_test == 'Positive' and donation.status == 'Pending' :
                donation.status = 'Rejected' 
                donation.save()
                ## send email to the donor
                send_rejection_email(donor)
                    
            elif blood_virus_test == 'Negative' and donation.status == 'Pending':
                donation.status = 'Accepted' 
                donation.save()
                ## add new blood bag in blood stock
                blood= BloodStock()
                blood.quantity = donation.quantity
                blood.blood_bank_city = donation.donor.city
                blood.blood_type = donation.donor.blood_type
                blood.save()
                messages.add_message(request, messages.SUCCESS, 'Donation was accepted and successfully stored at blood stock.')
                
        return HttpResponseRedirect(reverse("donor", kwargs={'id': donor.pk}))  # reverse because we don't know the id
    
    return render(request, 'donor/edit_donor.html',context)


########################################################

# @staff_required(login_url='/')
# def delete_donor(request, id):
#     donor = get_object_or_404(Donor, pk=id)
#     context = {'donor':donor}
#     if request.method == 'POST':
#         donor.delete()
#         messages.add_message(request, messages.SUCCESS, 'Donor was deleted successfully')
#         return HttpResponseRedirect(reverse('donors'))
#     return render(request, 'donor/delete_donor.html', context)


########################################################

@staff_required(login_url='/')
def search_donors(request):
    if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            donors = DonorUser.objects.filter(national_id__startswith= search_str 
                        ) | DonorUser.objects.filter(
                        city__name__istartswith=search_str )| DonorUser.objects.filter(
                        blood_virus_test__istartswith=search_str)
            donor_list = []
            for donor in donors:
                donor_list.append({
                "id": donor.id,
                "name": donor.name,
                "national_id": donor.national_id,
                "city": donor.city.name,
                "blood_type": donor.blood_type.name,
                "blood_virus_test": donor.blood_virus_test,
                })
            print(len(donor_list))
            return JsonResponse(donor_list, safe=False) # safe parameter for parsing list {not object} data without problems


########################################################


def donation_list(request):
    context1 = who(request)
    if request.user.is_staff:
        donation_list = Donation.objects.all()
    else:
        donation_list = Donation.objects.filter(donor__user=request.user)
    # donations = Donation.objects.filter(status='Pending')
    # if donations:
    #     for donation in donations:
    #         print('don')
    #         if donation.donor.blood_virus_test == "Negative":
    #             print('don')
    #             donation.status = "Accepted"
    #             donation.save()
    #             BloodStock.objects.create(blood_bank_city= donation.donor.city, blood_type= donation.donor.blood_type, quantity= donation.quantity)
    paginator = Paginator(donation_list, 20)
    pg_number = request.GET.get('page')
    pg_object = Paginator.get_page(paginator,pg_number)
    context = {
        'donations':donation_list,
        "pg_object":pg_object,
    }
    context.update(context1)
    return render(request, 'donation/donation_list.html',context)


########################################################


@require_http_methods(["POST"])
def validate_donor_for_donation(request):
    data = json.loads(request.body)
    print(data)
    national_id = data['national_id']
    donor = DonorUser.objects.filter(national_id = national_id)
    if not donor:
        return JsonResponse({'national_id_error': "There isn't a donor with this national ID"})
    elif not donor[0].last_donation_date or days_between(str(donor[0].last_donation_date) )/30 >3:
        donor.can_donate = True
        donor[0].save()
    
    if not donor[0].can_donate :
        return JsonResponse({'national_id_error': 'The donor must not donate before 3 months from last dontion date'})
    
    return JsonResponse({'national_id_valid': True})


########################################################


@staff_required(login_url='/')
def add_donation(request):
    form = DonationForm()
    context={
        'form': form,
    }
    
    if request.method == 'POST':
        donor_national_id = request.POST.get('naitonal_id')
        quantity = request.POST.get('quantity')
        donor = DonorUser.objects.get(national_id=donor_national_id)
        donation = Donation()
        donation.quantity = quantity
        donation.donor = donor
        donation.status = 'Pending'
        donation.save()
        donor.last_donation_date = datetime.today()
        donor.can_donate = False
        donor.save()
        messages.add_message(request, messages.SUCCESS, 'The donation process has been saved successfully.')
        return HttpResponseRedirect(reverse('donation', kwargs={'id':donation.pk}) )
    return render(request, 'donation/add_donation.html', context)


########################################################

@staff_required(login_url='/')
def donation_details(request,id):
    context1 = who(request)
    donation = Donation.objects.get(pk=id)
    context = {'donation':donation}
    context.update(context1)
    return render(request, 'donation/donation_details.html', context)


########################################################


@staff_required(login_url='/')
def blood_stock(request):
    blood_banks = BloodStock.objects.filter(expiration_date__gt= Now())
    paginator = Paginator(blood_banks, 20)
    pg_number = request.GET.get('page')
    pg_object = Paginator.get_page(paginator,pg_number)
    context = {
        'blood_banks':blood_banks,
        "pg_object":pg_object,
    }
    return render(request, 'blood_stock/blood_banks.html',context)





@staff_required(login_url='/')
def search_blood_stock(request):
    if request.method == 'POST':
            search_str = json.loads(request.body).get('searchText')
            bloods = BloodStock.objects.filter(expiration_date__gt= Now(), blood_type__name__iexact= search_str 
                        ) | BloodStock.objects.filter(expiration_date__gt= Now(),
                        blood_bank_city__name__icontains=search_str )
            blood_list = []
            for blood in bloods:
                blood_list.append({
                "id": blood.id,
                "expiration_date": blood.expiration_date,
                "quantity": blood.quantity,
                "blood_bank_city": blood.blood_bank_city.name,
                "blood_type": blood.blood_type.name,
                })
            return JsonResponse(blood_list, safe=False) # safe parameter for parsing list {not object} data without problems

