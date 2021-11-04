from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='home' ),
    path('donor/<int:id>/', views.donor_details, name='donor' ),
    path('add-donor', views.add_donor, name='add-donor' ),
    path('edit-donor/<int:id>', views.edit_donor, name='edit-donor' ),
    path('delete-donor/<int:id>', views.delete_donor, name='delete-donor' ),
    path('search-donors', csrf_exempt(views.search_donors),name="search_donors"),
]