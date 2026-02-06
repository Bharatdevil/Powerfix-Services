from django.shortcuts import render, redirect,get_object_or_404
from bookings.models import Booking
from services.models import Service
from accounts.models import Customer, Electrician
from django.db.models import Sum
from django.db.models.functions import TruncDate

def admin_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('admin_login')

    context = {
        'pending_count': Booking.objects.filter(status='Pending').count(),
        'assigned_count': Booking.objects.filter(status='Assigned').count(),
        'completed_count': Booking.objects.filter(status='Completed').count(),
        'paid_count': Booking.objects.filter(status='Paid').count(),
    }

    return render(request, 'admin/admin_dashboard.html', context)


 # <=================== Admin Services ==================>
def admin_services(request):
    services = Service.objects.all()
    # electricians = Electrician.objects.all()

    if request.method == 'POST':
        name = request.POST.get('s_name')
        description = request.POST.get('s_description')
        price = request.POST.get('s_price')
        #electrician_id = request.POST.get('electrician')

        #electrician = Electrician.objects.get(id=electrician_id)

        Service.objects.create(
            s_name=name,
            s_description=description,
            s_price=price,
         #e_id=electrician
        )

        return redirect('admin_services')
 
    return render(request, 'admin/view_services.html', {
        'services': services,
        #'electricians': electricians
    })

def update_service(request, pk):
    service = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        service.s_name = request.POST['s_name']
        service.s_description = request.POST['s_description']
        service.s_price = request.POST['s_price']
        service.save()
        return redirect('admin_services')

    return render(request, 'admin/update_service.html', {
        'service': service
    })


def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('admin_services')
# <=================== Admin Services End ==================>



# <=================== Admin Bookings ==================>
def admin_bookings(request):
    status = request.GET.get('status')

    bookings = Booking.objects.all().order_by('-id')
    if status:
        bookings = bookings.filter(status=status)

    electricians = Electrician.objects.all() 

    return render(request, 'admin/admin_booking.html', {
        'bookings': bookings,
        'electricians': electricians, 
        'selected_status': status
    })

def assign_electrician(request, booking_id):
    if 'admin_id' not in request.session:
        return redirect('login')

    booking = get_object_or_404(Booking, id=booking_id)
    electricians = Electrician.objects.all()
    print(electricians)

    if request.method == 'POST':
        electrician_id = request.POST.get('electrician')

        booking.electrician_id = electrician_id
        booking.status = 'Assigned'
        booking.save()
        Electrician.objects.filter(id=electrician_id).update(status="Busy")

        return redirect('admin_bookings')

    return render(request, 'admin/assign_electrician.html', {
        'bookings': booking,
        'electricians': electricians,
     }) 

# <=================== Admin Bookings End ==================>




# <=================== Admin Electrician ======================>
def admin_electricians(request):
    electricians = Electrician.objects.all()

    if request.method == 'POST':
        Electrician.objects.create(
            e_fullname=request.POST['fullname'],
            e_qualification=request.POST['qualification'],
            e_email=request.POST['email'],
            e_contact=request.POST['contact'],
            e_address=request.POST['address'],
            e_login_id=request.POST['login_id'],
            e_password=request.POST['password']
        )
        return redirect('admin_electricians')

    return render(request, 'admin/view_electricians.html', {
        'electricians': electricians
    })

def view_electricians(request):
    electricians = Electrician.objects.all()
    return render(request, 'admin/view_electricians.html', {
        'electricians': electricians
    })
def update_electrician(request, id):
    electrician = Electrician.objects.get(id=id)
    print(electrician)

    if request.method == 'POST':
        electrician.e_contact = request.POST.get('contact')
        electrician.e_address = request.POST.get('address')
        electrician.save()
        return redirect('admin_electricians')

    return render(request, 'admin/update_electrician.html', {
        'electrician': electrician
    })

def delete_electrician(request, id):
    electrician = Electrician.objects.get(id=id)
    electrician.delete()
    return redirect('admin_electricians')


# <=================== Admin Electrician End ==================>

# <=================== Admin Reports ==================>
from django.utils import timezone
from datetime import timedelta
PLATFORM_PERCENT = 15
def admin_revenue_report(request):
    period = request.GET.get('period', '7days')

    today = timezone.now().date()

    if period == 'today':
        start_date = today
    elif period == 'yesterday':
        start_date = today - timedelta(days=1)
    elif period == 'month':
        start_date = today.replace(day=1)
    else:  # last 7 days (default)
        start_date = today - timedelta(days=6)

    bookings = Booking.objects.filter(
        status='Paid',
        booking_date__gte=start_date
    )

    # 1️⃣ Date-wise customer revenue (BAR)
    date_data = bookings.annotate(
        day=TruncDate('booking_date')
    ).values('day').annotate(
        total=Sum('total_amount')
    ).order_by('day')

    dates = [str(d['day']) for d in date_data]
    revenues = [d['total'] for d in date_data]

    # 2️⃣ Service-wise revenue (PIE)
    service_data = bookings.values(
        'service__s_name'
    ).annotate(
        total=Sum('total_amount')
    )

    services = [s['service__s_name'] for s in service_data]
    service_amounts = [s['total'] for s in service_data]

    # 3️⃣ Revenue split (PIE)
    total_customer_paid = bookings.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    electrician_share = int(total_customer_paid * (100 - PLATFORM_PERCENT) / 100)
    platform_share = total_customer_paid - electrician_share

    context = {
        'dates': dates,
        'revenues': revenues,
        'services': services,
        'service_amounts': service_amounts,
        'electrician_share': electrician_share,
        'platform_share': platform_share,
        'selected_period': period
    }

    return render(request, 'admin/revenue_report.html', context)
# <=================== Admin Reports End ==================>
