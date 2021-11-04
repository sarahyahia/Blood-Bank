from django.contrib import admin
from .models import City



class CityAdmin(admin.ModelAdmin):
    list_display = ['name','longitude','latitude']
    search_fields = ( 'name',)
    list_per_page = 20

admin.site.register(City,CityAdmin)