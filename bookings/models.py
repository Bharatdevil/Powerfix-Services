from django.db import models 
from accounts.models import Customer, Electrician
from services.models import Service

# Create your models here.
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    electrician = models.ForeignKey(Electrician, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        default="Pending"
    )  # Pending / Assigned / Completed / Paid

    base_price = models.IntegerField()
    total_amount = models.IntegerField(null=True, blank=True)
    electrician_earning = models.IntegerField(default=0)

    booking_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="items")

    item_name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    total_price = models.IntegerField()
