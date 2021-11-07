from django.contrib import admin
from .models import Request


class RequestAdmin(admin.ModelAdmin):
    list_display = ['hospital','blood_type','request_status']
    search_fields = ( 'hospital','blood_type','request_status',)
    list_per_page = 20


admin.site.register(Request,RequestAdmin)