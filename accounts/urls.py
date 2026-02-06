from django.urls import path
from .views import *


urlpatterns = [
    #customer urls
    path('customer_login/', customer_login, name='customer_login'),   
    path('customer_logout/',customer_logout, name='customer_logout'),
    path('customer/profile/', customer_profile, name='customer_profile'),
    path('register/', customer_register, name='customer_register'),    

    #electrician urls
    path('electrician_login/', electrician_login, name='electrician_login'),
    path('electrician_logout/',electrician_logout, name='electrician_logout'),


    # admin urls
    path('admin/login/', admin_login, name='admin_login'),
     path('admin_logout/',admin_logout, name='admin_logout'),
    #path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    #path('admin/services/', admin_services, name='admin_services'),
    #path('admin/service/update/<int:pk>/', update_service, name='update_service'),
    #path('admin/service/delete/<int:pk>/', delete_service, name='delete_service'),
    #path('admin/electricians/', admin_electricians, name='admin_electricians'),
    #path('admin/electrician/update/<int:id>/', update_electrician, name='update_electrician'),
    #path('admin/electrician/delete/<int:id>/', delete_electrician, name='delete_electrician'),



    #services 
    #path('admin/add-service/',add_service, name='add_service'),

]    
