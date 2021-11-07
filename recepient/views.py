from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Request
from donor.models import BloodType
from authentication.models import HospitalUser
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages



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
        blood_request = Request()
        blood_request.quantity = quantity
        blood_request.blood_type = blood_type
        blood_request.hospital =hospital
        blood_request.request_status = 'Pending'
        blood_request.patient_status = patient_status
        
        blood_request.save()
        messages.add_message(request, messages.SUCCESS, f'request with number {blood_request.id} has been sent')
        return HttpResponseRedirect(reverse("request", kwargs={'id': request.pk}))
    return render(request, 'recepient/add_request.html', context)




def request_details(request, id):
    blood_request = Request.objects.get(pk = id)
    context = {
        'blood_request': blood_request,
    }
    return render(request, 'recepient/request_details.html', context)




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
        messages.add_message(request, messages.SUCCESS, f'request with number {id} has been edited')
        return HttpResponseRedirect(reverse("request", kwargs={'id': id}))
    return render(request, 'recepient/edit_request.html', context)



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