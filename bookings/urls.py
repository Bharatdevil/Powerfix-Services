from django.urls import path
from .views import *

urlpatterns = [
    path('book/<int:service_id>/', book_service, name='book_service'),
    path('my-bookings/', customer_bookings, name='customer_bookings'),
    path('invoice/<int:booking_id>/',customer_invoice,name='customer_invoice'),
]
