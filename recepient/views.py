from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Request
from donor.models import BloodType, BloodStock
from authentication.models import HospitalUser
from authentication.views import who
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
import geopy.distance
from django.db.models.functions import Now
import threading
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from helpers.decorators import staff_required
from django.contrib.auth.decorators import login_required


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()



########################################################



def send_response_email(request,matched_blood=None):
    if request.request_status == 'Accepted':
        htmly = get_template('recepient/Email.html')
    elif request.request_status == 'Rejected':
        htmly = get_template('recepient/rejectEmail.html')
        
    context = {
        'request':request,
        'matched_blood':matched_blood
    }
    subject, from_email,to = 'Blood Request Results', settings.EMAIL_HOST_USER, request.hospital.user.email
    html_content = htmly.render(context)
    email = EmailMultiAlternatives(subject, html_content, from_email, [to])
    email.attach_alternative(html_content, "text/html")
    if not settings.TESTING:
        EmailThread(email).start()


########################################################


@login_required(redirect_field_name='/')
def index(request):
    context1 = who(request)
    if request.user.is_staff:
        requests = Request.objects.all()
        pending_requests = Request.objects.filter(request_status='Pending').count
    else:
        requests = Request.objects.filter(hospital__user= request.user)
        pending_requests = 0
    paginator = Paginator(requests, 10)
    pg_number = request.GET.get('page')
    pg_object = Paginator.get_page(paginator,pg_number)
    context ={
        'requests': requests,
        "pg_object":pg_object,
        'pending_requests':pending_requests
    }
    context.update(context1)
    return render(request, 'recepient/index.html', context)



@login_required(redirect_field_name='/')
def add_request(request):
    context1 = who(request)
    blood_types = BloodType.objects.all()
    context = {
        'blood_types': blood_types,
        'blood_request': request.POST,
    }
    context.update(context1)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        patient_status = request.POST.get('patient_status')     
        blood_type_instance= request.POST.get('blood_type')
        blood_type = BloodType.objects.get(pk=blood_type_instance)
        hospital = HospitalUser.objects.get(user = request.user)
        if not quantity or not blood_type or not patient_status:
            messages.add_message(request, messages.ERROR, 'You should fill all fields')
            return render(request, 'recepient/add_request.html', context)
        if int(quantity)<0 :
            messages.add_message(request, messages.ERROR, 'Quantity must be a positive number')
            return render(request, 'recepient/add_request.html', context)
        blood_request = Request()
        blood_request.quantity = quantity
        blood_request.blood_type = blood_type
        blood_request.hospital =hospital
        blood_request.request_status = 'Pending'
        blood_request.patient_status = patient_status
        
        blood_request.save()
        if Request.objects.filter(request_status='Pending').count() >= 10:
            handle_request_automatically()
        messages.add_message(request, messages.SUCCESS, f'request with number {blood_request.id} has been sent')
        return HttpResponseRedirect(reverse("request", kwargs={'id': blood_request.pk}))
    return render(request, 'recepient/add_request.html', context)




@login_required(redirect_field_name='/')
def request_details(request, id):
    context1 = who(request)
    blood_request = Request.objects.get(pk = id)
    context = {
        'blood_request': blood_request,
    }
    context.update(context1)
    return render(request, 'recepient/request_details.html', context)




@login_required(redirect_field_name='/')
def edit_request(request, id):
    context1 = who(request)
    blood_types = BloodType.objects.all()
    blood_request = Request.objects.get(pk=id)
    if request.user != blood_request.hospital.user:
        return redirect('requests')
    context = {
        'blood_types': blood_types,
        'blood_request': blood_request,
    }
    context.update(context1)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        patient_status = request.POST.get('patient_status')     
        blood_type_instance= request.POST.get('blood_type')
        blood_type = BloodType.objects.get(pk=blood_type_instance)
        hospital = HospitalUser.objects.get(user = request.user)
        if not quantity or not blood_type or not patient_status:
            messages.add_message(request, messages.ERROR, 'You should fill all fields')
            return render(request, 'recepient/edit_request.html', context)
        blood_request.quantity = quantity
        blood_request.blood_type = blood_type
        blood_request.patient_status = patient_status
        
        blood_request.save()
        messages.add_message(request, messages.SUCCESS, f'request with number {id} has been edited')
        return HttpResponseRedirect(reverse("request", kwargs={'id': id}))
    return render(request, 'recepient/edit_request.html', context)



@login_required(redirect_field_name='/')
def delete_request(request, id):
    context1 = who(request)
    blood_request = Request.objects.get(pk=id)
    context = {
        'blood_request': blood_request,
    }
    if request.method == 'POST':
        blood_request.delete()
        messages.add_message(request, messages.SUCCESS, f'request with number {id} has been deleted')
        return redirect('requests')
    context.update(context1)
    return render(request, 'recepient/delete_request.html', context)



def calc_distance(city1, city2):
    coordinates1 = (city1.latitude, city1.longitude)
    coordinates2 = (city2.latitude, city2.longitude)
    least_distance = geopy.distance.distance(coordinates1, coordinates2).km
    return least_distance


def blood_compitability(blood_type):
    if blood_type == 'A+':
        blood_group = ['A+', 'A-', 'O+', 'O-']
    elif blood_type == 'A-':
        blood_group = ['A-', 'O-']
    elif blood_type == 'B+':
        blood_group = ['B+', 'B-', 'O+', 'O-']
    elif blood_type == 'B-':
        blood_group =['B-', 'O-']
    elif blood_type == 'AB+':
        blood_group = ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-']
    elif blood_type == 'AB-':
        blood_group = ['AB-', 'A-', 'B-', 'O-']
    elif blood_type == 'O-':
        blood_group = ['O-']
    else:
        blood_group = [ 'O+', 'O-']
    blood_available_by_type = BloodStock.objects.filter(expiration_date__gt= Now(), blood_type__name__in= blood_group)
    return blood_available_by_type


def get_matched_query_for_request(request):
    blood_available_by_type = list(blood_compitability(request.blood_type.name))
    for _ in range(len(blood_available_by_type)):
        min_distance = calc_distance(request.hospital.city, blood_available_by_type[0].blood_bank_city)
        min_distance_index = 0
        for i in range(len(blood_available_by_type)):
            distance = calc_distance(request.hospital.city, blood_available_by_type[i].blood_bank_city)
            if distance < min_distance :
                min_distance = distance
                min_distance_index = i
        matched_blood = blood_available_by_type[min_distance_index]
        if request.quantity <= matched_blood.quantity:
            quantity_diff = matched_blood.quantity - request.quantity
            print(min_distance)
            return {
                'matched_blood_record': matched_blood, 
                'request':request, 
                'min_distance': min_distance,
                'patient_status':request.patient_status, 
                'blood_type':matched_blood.blood_type.name
            }
        elif request.quantity > matched_blood.quantity:
            blood_available_by_type.pop(min_distance_index)
    request.request_status = 'Rejected'
    request.save()
    return None

def get_sorted_pending_requests():
    temp_acceptable = []
    requests = Request.objects.filter(request_status='Pending').order_by('date')
    for request in requests:
        result = get_matched_query_for_request(request)
        if result:
            temp_acceptable.append(result)
    temp_acceptable = sorted(temp_acceptable, key = lambda i: (i['blood_type'], i['min_distance'], i['patient_status']))
    print(temp_acceptable)
    return temp_acceptable


def handle_request_automatically():
    while get_sorted_pending_requests().count:
        for request in get_sorted_pending_requests():
            try:
                request['matched_blood_record']= BloodStock.objects.get(pk=request['matched_blood_record'].pk)
                if request['matched_blood_record'].quantity - request['request'].quantity >= 0:
                    quantity_diff = request['matched_blood_record'].quantity - request['request'].quantity
                    request['request'].request_status = 'Accepted'
                    request['request'].save()
                    request['matched_blood_record'].quantity = quantity_diff
                    if not quantity_diff :
                        print(quantity_diff)
                        request['matched_blood_record'].delete()
                    else:
                        print(quantity_diff, 'else')
                        request['matched_blood_record'].save()
                elif not get_matched_query_for_request(request['request']):
                    continue
            except BloodStock.DoesNotExist:
                handle_request_automatically()
        return True




@staff_required(login_url='/')
def handle_requests(request= None):
    if handle_request_automatically():
        messages.add_message(request ,messages.SUCCESS, 'All Requests got handled successfully.')
    return redirect('requests')
