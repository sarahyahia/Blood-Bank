from django.contrib import admin
from .models import Donor, BloodType


class DonorAdmin(admin.ModelAdmin):
    list_display = ['name','national_id','city']
    search_fields = ( 'name','national_id','city',)
    list_per_page = 20

admin.site.register(Donor,DonorAdmin)
admin.site.register(BloodType)