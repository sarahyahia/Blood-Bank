from django.contrib import admin
from .models import Donor, BloodType, Donation, BloodStock


class DonorAdmin(admin.ModelAdmin):
    list_display = ['name','national_id','city']
    search_fields = ( 'name','national_id','city',)
    list_per_page = 20

class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor','quantity','status']
    search_fields = ( 'donor','quantity','status',)
    list_per_page = 20


class BloodStockAdmin(admin.ModelAdmin):
    list_display = ['blood_type','quantity','expiration_date']
    search_fields = ( 'blood_type','quantity','expiration_date',)
    list_per_page = 20

admin.site.register(Donor,DonorAdmin)
admin.site.register(BloodType)
admin.site.register(BloodStock, BloodStockAdmin)
admin.site.register(Donation,DonationAdmin)