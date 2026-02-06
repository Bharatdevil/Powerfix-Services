from django.shortcuts import render, redirect,get_object_or_404
from bookings.models import Booking,BookingItem
from accounts.models import Electrician
from django.db.models import Sum
from django.contrib import messages

# electrician dashboard and profile


def electrician_profile(request):
    if not request.session.get('electrician_id'):
        return redirect('home')

    electrician = Electrician.objects.get(id=request.session['electrician_id'])

    if request.method == 'POST':
        electrician.e_fullname = request.POST.get('name')
        electrician.e_qualification = request.POST.get('qualification')
        electrician.e_contact = request.POST.get('contact')
        electrician.e_address = request.POST.get('address')
        electrician.save()
        return redirect('electrician_dashboard')

    return render(request, 'electrician/electrician_profile.html', {
        'electrician': electrician
    })

def electrician_bookings(request):
    electrician_id = request.session.get('electrician_id')
    if not electrician_id:
        return redirect('electrician_login')

    electrician = Electrician.objects.get(id=electrician_id)

    status = request.GET.get('status', 'Assigned')

    bookings = Booking.objects.filter(
        electrician=electrician,
        status=status
    ).order_by('-id')

    return render(request, 'electrician/electrician_bookings.html', {
        'bookings': bookings,
        'selected_status': status
    })


def electrician_dashboard(request):
    electrician_id = request.session.get('electrician_id')
    if not electrician_id:
        return redirect('electrician_login')

    electrician = Electrician.objects.get(id=electrician_id)

    assigned_count = Booking.objects.filter(
        electrician=electrician,
        status='Assigned'
    ).count()

    completed_count = Booking.objects.filter(
        electrician=electrician,
        status='Completed'
    ).count()

    total_earnings = Booking.objects.filter(
        electrician=electrician,
        status='Paid'
    ).aggregate(
        total=Sum('electrician_earning')
    )['total'] or 0

    return render(request, 'electrician/electrician_dashboard.html', {
        'assigned_count': assigned_count,
        'completed_count': completed_count,
        'total_earnings': total_earnings
    })


def complete_job(request, booking_id):
    electrician_id = request.session.get('electrician_id')
    if not electrician_id:
        return redirect('electrician_login')

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        electrician_id=electrician_id,
        status='Assigned'
    )

    if request.method == 'POST':
        item_names = request.POST.getlist('item_name')
        quantities = request.POST.getlist('quantity')
        prices = request.POST.getlist('unit_price')

        extra_total = 0

        for name, qty, price in zip(item_names, quantities, prices):
            if name and qty and price:
                total_price = int(qty) * int(price)

                BookingItem.objects.create(
                    booking=booking,
                    item_name=name,
                    quantity=int(qty),
                    unit_price=int(price),
                    total_price=total_price
                )

                extra_total += total_price

        booking.total_amount = booking.base_price + extra_total
        booking.status = 'Completed'
        booking.save()

        electrician = booking.electrician
        electrician.status = 'Available'
        electrician.save()
        
        messages.success(request, "Job marked as completed successfully")
        return redirect('electrician_bookings')

    return render(request, 'electrician/complete_job.html', {
        'booking': booking
    })



def electrician_earnings(request):
    electrician_id = request.session.get('electrician_id')
    if not electrician_id:
        return redirect('electrician_login')

    # All PAID jobs of this electrician
    paid_jobs = Booking.objects.select_related(
        'customer', 'service'
    ).filter(
        electrician_id=electrician_id,
        status='Paid'
    ).order_by('-booking_date')

    total_earnings = paid_jobs.aggregate(
        total=Sum('electrician_earning')
    )['total'] or 0

    context = {
        'paid_jobs': paid_jobs,
        'total_earnings': total_earnings,
        'jobs_count': paid_jobs.count()
    }

    return render(request, 'electrician/electrician_earnings.html', context)