from django.urls import path ,include
from .views import *
app_name = "payments"
urlpatterns = [
    path("checkout/<int:booking_id>/",start_payment,name="start_payment"),
    path("success/", payment_success, name="payment_success"),
        path("invoice/pdf/<int:booking_id>/",download_invoice_pdf,name="download_invoice_pdf"),

]