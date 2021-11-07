from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='donors' ),
    path('donor/<int:id>/', views.donor_details, name='donor' ),
    path('add-donor/', views.add_donor, name='add-donor' ),
    path('edit-donor/<int:id>', views.edit_donor, name='edit-donor' ),
    path('delete-donor/<int:id>', views.delete_donor, name='delete-donor' ),
    path('search-donors', csrf_exempt(views.search_donors),name="search_donors"),
    
    ## donations
    path('donations/', views.donation_list, name='donations' ),
    path('donations/donation/<int:id>/', views.donation_details, name='donation' ),
    path('donations/add-donation/', views.add_donation, name='add-donation' ),
    path('donations/validate-donor', csrf_exempt(views.validate_donor_for_donation), name="validate-donor"),
    
    # blood_stock
    path('blood-stock/', views.blood_stock, name='blood-stock' ),
    
]