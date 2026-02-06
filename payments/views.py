import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from bookings.models import Booking,BookingItem
from .models import Payment
import json
from django.http import JsonResponse,HttpResponse
from django.utils import timezone
from .models import Payment, Invoice
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def start_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": booking.total_amount * 100,  # paise
        "currency": "INR",
        "payment_capture": 1
    })

    payment = Payment.objects.create(
        booking=booking,
        razorpay_order_id=order["id"],
        amount=booking.total_amount,
        payment_type="UPI",
        status="Created"
    )

    return render(request, "payments/checkout.html", {
        "booking": booking,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order_id": order["id"],
        "amount": booking.total_amount
    })




def payment_success(request):
    data = json.loads(request.body)

    # Get payment
    payment = Payment.objects.get(
        razorpay_order_id=data["razorpay_order_id"]
    )

    # Update payment details
    payment.razorpay_payment_id = data["razorpay_payment_id"]
    payment.razorpay_signature = data["razorpay_signature"]
    payment.status = "Success"
    payment.paid_at = timezone.now()
    payment.save()

    # Update booking status
    booking = payment.booking
    booking.status = "Paid"
    PLATFORM_PERCENT = 15
    customer_paid = booking.total_amount
    booking.electrician_earning = int(
        customer_paid * (100 - PLATFORM_PERCENT) / 100
    )
    booking.save()

    # Create invoice only once (no PDF stored)
    Invoice.objects.get_or_create(
        booking=booking,
        defaults={
            "invoice_number": f"INV-{booking.id}",
            "total_amount": booking.total_amount,
            "payment_status": "Paid",
        }
    )

    return JsonResponse({"status": "success"})


def download_invoice_pdf(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    invoice = Invoice.objects.get(booking=booking)
    items = BookingItem.objects.filter(booking=booking)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="invoice_{invoice.invoice_number}.pdf"'
    )

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 40

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Powerfix Services - Invoice")

    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Invoice No: {invoice.invoice_number}")
    c.drawString(350, y, f"Date: {invoice.invoice_date}")

    y -= 30
    c.drawString(40, y, f"Service: {booking.service.s_name}")
    y -= 15
    c.drawString(40, y, f"Booking Date: {booking.booking_date}")
    y -= 15
    c.drawString(40, y, f"Status: {booking.status}")

    # Table Header
    y -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Item")
    c.drawString(300, y, "Qty")
    c.drawString(350, y, "Price")
    c.drawString(430, y, "Total")

    y -= 10
    c.line(40, y, 550, y)

    # Items
    c.setFont("Helvetica", 10)
    for item in items:
        y -= 20
        c.drawString(40, y, item.item_name)
        c.drawString(300, y, str(item.quantity))
        c.drawString(350, y, f"₹{item.unit_price}")
        c.drawString(430, y, f"₹{item.total_price}")

    # Totals
    # Totals section
    y -= 30
    c.drawString(350, y, f"Base Price: ₹{booking.base_price}")

    y -= 20
    extra_total = sum(item.total_price for item in items)
    c.drawString(350, y, f"Extra Materials: ₹{extra_total}")

    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(350, y, f"Total Amount: ₹{booking.total_amount}")

    c.showPage()
    c.save()

    return response