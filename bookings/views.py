from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404,render
from services.models import Service
from .models import Booking


def book_service(request, service_id):
    if 'customer_id' not in request.session:
        return redirect('login')

    if request.method == "POST":
        service = get_object_or_404(Service, id=service_id)

        Booking.objects.create(
            customer_id=request.session['customer_id'],
            service=service,
            base_price=service.s_price,
            status="Pending"
        )

        return redirect('customer_bookings')
    
def customer_bookings(request):
    if 'customer_id' not in request.session:
        return redirect('home')

    bookings = Booking.objects.filter(
        customer_id=request.session['customer_id']
    ).order_by('-id')

    return render(request, 'bookings/bookings.html', {
        'bookings': bookings
    })

def customer_invoice(request, booking_id):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('home')

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer_id=customer_id,
        status__in=['Completed', 'Paid']
    )

    items = booking.items.all()

    extra_total = sum(item.total_price for item in items)

    return render(request, 'payments/invoice.html', {
        'booking': booking,
        'items': items,
        'extra_total': extra_total,
        "today": timezone.now().date()
    })