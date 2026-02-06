from django.urls import path
from  .views import *

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),

    path('bookings/', admin_bookings, name='admin_bookings'),
    path('bookings/assign/<int:booking_id>/', assign_electrician, name='assign_electrician'),

    path('services/', admin_services, name='admin_services'),
    path('service/update/<int:pk>/', update_service, name='update_service'),
    path('service/delete/<int:pk>/', delete_service, name='delete_service'),


    path('electricians/', admin_electricians, name='admin_electricians'),
    path('electrician/update/<int:id>/', update_electrician, name='update_electrician'),
    path('electrician/delete/<int:id>/', delete_electrician, name='delete_electrician'),
    
    path('revenue-report/', admin_revenue_report, name='admin_revenue_report'),


]
