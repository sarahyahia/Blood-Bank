from django.contrib import admin
from .models import HospitalUser, DonorUser


class HospitalUserAdmin(admin.ModelAdmin):
    list_display = ['hospital_name','user','city']
    search_fields = ( 'hospital_name','user','city',)
    list_per_page = 20


class DonorUserAdmin(admin.ModelAdmin):
    list_display = ['name','user','city']
    search_fields = ( 'name','user','city',)
    list_per_page = 20

admin.site.register(HospitalUser,HospitalUserAdmin)
admin.site.register(DonorUser,DonorUserAdmin)
