from django.db import models
from bookings.models import Booking
# Create your models here.
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)

    amount = models.IntegerField()
    payment_type = models.CharField(max_length=30)  # UPI / Card / NetBanking
    status = models.CharField(max_length=20, default="Created")  # Created / Success / Failed

    paid_at = models.DateTimeField(null=True, blank=True)


class Invoice(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_date = models.DateField(auto_now_add=True)
    total_amount = models.IntegerField()

    payment_status = models.CharField(max_length=20, default="Unpaid")
   

    created_at = models.DateTimeField(auto_now_add=True)
