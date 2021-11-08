from django.urls import path
from . import views

urlpatterns = [
    path('', views.index ,name='requests'),
    path('request/<int:id>', views.request_details, name='request'),
    path('add-request/', views.add_request, name='add-request'),
    path('edit-request/<int:id>', views.edit_request, name='edit-request'),
    path('delete-request/<int:id>', views.delete_request, name='delete-request'),
    path('handle-requests/', views.handle_requests, name='handle-requests'),

]