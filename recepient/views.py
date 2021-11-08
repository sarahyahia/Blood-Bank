from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Request
from donor.models import BloodType, BloodStock
from authentication.models import HospitalUser
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
    if request.user.is_staff:
        requests = Request.objects.all()
    else:
        requests = Request.objects.filter(hospital__user= request.user)
    paginator = Paginator(requests, 5)
    pg_number = request.GET.get('page')
    pg_object = Paginator.get_page(paginator,pg_number)
    context ={
        'requests': requests,
        "pg_object":pg_object,
    }
    return render(request, 'recepient/index.html', context)



@login_required(redirect_field_name='/')
def add_request(request):
    blood_types = BloodType.objects.all()
    context = {
        'blood_types': blood_types,
        'blood_request': request.POST,
    }
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        patient_status = request.POST.get('patient_status')     
        blood_type_instance= request.POST.get('blood_type')
        blood_type = BloodType.objects.get(pk=blood_type_instance)
        hospital = HospitalUser.objects.get(user = request.user)
        if not quantity or not blood_type or not patient_status:
            messages.add_message(request, messages.ERROR, 'You should fill all fields')
            return render(request, 'recepient/add_request.html', context)
        if int(quantity)> 4 or int(quantity)< 1 :
            messages.add_message(request, messages.ERROR, 'Quantity must be between 1-4 bags')
            return render(request, 'recepient/add_request.html', context)
        blood_request = Request()
        blood_request.quantity = quantity
        blood_request.blood_type = blood_type
        blood_request.hospital =hospital
        blood_request.request_status = 'Pending'
        blood_request.patient_status = patient_status
        
        blood_request.save()
        messages.add_message(request, messages.SUCCESS, f'request with number {blood_request.id} has been sent')
        if patient_status == 'Immediate':
            # threading.Thread(target=create_transaction,args=[blood_request])
            create_transaction(blood_request)
        return HttpResponseRedirect(reverse("request", kwargs={'id': blood_request.pk}))
    return render(request, 'recepient/add_request.html', context)




@login_required(redirect_field_name='/')
def request_details(request, id):
    blood_request = Request.objects.get(pk = id)
    context = {
        'blood_request': blood_request,
    }
    return render(request, 'recepient/request_details.html', context)




@login_required(redirect_field_name='/')
def edit_request(request, id):
    blood_types = BloodType.objects.all()
    blood_request = Request.objects.get(pk=id)
    if request.user != blood_request.hospital.user:
        return redirect('requests')
    context = {
        'blood_types': blood_types,
        'blood_request': blood_request,
    }
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
        if patient_status == 'Immediate':
            # threading.Thread(target=create_transaction,args=[blood_request])
            create_transaction(blood_request)
        messages.add_message(request, messages.SUCCESS, f'request with number {id} has been edited')
        return HttpResponseRedirect(reverse("request", kwargs={'id': id}))
    return render(request, 'recepient/edit_request.html', context)



@login_required(redirect_field_name='/')
def delete_request(request, id):
    blood_request = Request.objects.get(pk=id)
    context = {
        'blood_request': blood_request,
    }
    if request.method == 'POST':
        blood_request.delete()
        messages.add_message(request, messages.SUCCESS, f'request with number {id} has been deleted')
        return redirect('requests')
    return render(request, 'recepient/delete_request.html', context)



def calc_distance(city1, city2):
    coordinates1 = (city1.latitude, city1.longitude)
    coordinates2 = (city2.latitude, city2.longitude)
    least_distance = geopy.distance.distance(coordinates1, coordinates2).km
    return least_distance


def blood_compitability(blood_type):
    if blood_type == 'A+':
        return ['A+', 'A-', 'O+', 'O-']
    elif blood_type == 'A-':
        return ['A-', 'O-']
    elif blood_type == 'B+':
        return ['B+', 'B-', 'O+', 'O-']
    elif blood_type == 'B-':
        return ['B-', 'O-']
    elif blood_type == 'AB+':
        return ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-']
    elif blood_type == 'AB-':
        return ['AB-', 'A-', 'B-', 'O-']
    elif blood_type == 'O-':
        return ['O-']
    else:
        return [ 'O+', 'O-']



def optimized_response(request,min_distance):
    if min_distance['distance'] > 150:
        request.request_status = 'Rejected'
        request.save()
        send_response_email(request)
        return True
    matched_blood = BloodStock.objects.get(pk=min_distance['id'])
    if int(request.quantity) == matched_blood.quantity:
        request.request_status = 'Accepted'
        request.save()
        send_response_email(request, matched_blood)
        matched_blood.delete()
        return True
    elif matched_blood.quantity > int(request.quantity):
        request.request_status = 'Accepted'
        request.save()
        matched_blood.quantity -= int(request.quantity)
        matched_blood.save()
        send_response_email(request, matched_blood)
        return True
    
    else:
        return False



def create_transaction(request):
    print(request.patient_status)
    blood_group = blood_compitability(request.blood_type.name)
    available_blood_by_type =[]
    for blood_type in blood_group:
        fresh_blood = list(BloodStock.objects.filter(expiration_date__gt= Now(), blood_type__name= blood_type))
        available_blood_by_type.append(fresh_blood)
    distance_list =[]
    for i in range(len(available_blood_by_type)):
        for j in range(len(available_blood_by_type[i])):
            distance = calc_distance(request.hospital.city, available_blood_by_type[i][j].blood_bank_city)
            distance_list.append({'id':available_blood_by_type[i][j].pk, 'distance':distance, 'blood_type':blood_group[i]})
    min_distance = min(distance_list, key=lambda x:x['distance'])
    
    if optimized_response(request, min_distance):
        return True
    else:
        distance_list = [i for i in distance_list if not (i == min_distance)]
        min_distance2 = min(distance_list, key=lambda x:x['distance'])
        matched_blood2 = BloodStock.objects.get(pk=min_distance2['id'])
        if matched_blood == matched_blood2 and int(request.quantity) <= (matched_blood.quantity+ matched_blood2.quantity):
            request.request_status = 'Accepted'
            request.save()
            send_response_email(request, matched_blood)
            matched_blood.delete()
            if int(request.quantity) == (matched_blood.quantity+ matched_blood2.quantity):
                matched_blood2.delete()
            else:
                matched_blood2.quantity = matched_blood.quantity+ matched_blood2.quantity - int(request.quantity)
                matched_blood2.save()
            return None
        
        elif not optimized_response(request,min_distance2):
            request.request.status = 'Rejected'
            request.save()
            send_response_email(request)
            return True


@staff_required(login_url='requests')
def handle_requests(request):
    requests = Request.objects.filter(request_status='Pending', patient_status='Urgent').order_by('date')
    for requeste in requests:
        create_transaction(requeste)
    
    requests = Request.objects.filter(request_status='Pending', patient_status='Normal').order_by('date')
    for requeste in requests:
        create_transaction(requeste)
    
    messages.add_message(request ,messages.SUCCESS, 'All Requests got handled successfully.')
    return redirect('requests')

