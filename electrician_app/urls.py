from django.urls import path
from .views import *

urlpatterns = [
    path('electrician/profile/', electrician_profile, name='electrician_profile'),
    path('bookings/', electrician_bookings, name='electrician_bookings'),
    path('dashboard/',electrician_dashboard, name='electrician_dashboard'),
    path('complete-job/<int:booking_id>/',complete_job,name='electrician_complete_job'),
    path('earnings/',electrician_earnings,name='electrician_earnings'),
]
