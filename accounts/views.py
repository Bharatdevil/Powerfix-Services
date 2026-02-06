from django.shortcuts import get_object_or_404, render, redirect
from .models import Customer, Electrician, AdminUser
from services.models import Service
from bookings.models import Booking
from django.contrib import messages



# <============= Customer Login =================>
def customer_login(request):
    if request.method == 'POST':
        login_id = request.POST.get('login_id')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(
                c_login_id=login_id,
                c_password=password
            )
            request.session['customer_id'] = customer.id
            messages.success(request, "Login successful!")
            return redirect('home')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid username or password')

    return redirect('home')

def customer_logout(request):
    request.session.pop('customer_id', None)
    return redirect('home')


# customer registration and profile
def customer_register(request):
    if request.method == 'POST':
        Customer.objects.create(
            c_fullname=request.POST.get('c_fullname'),
            c_login_id=request.POST.get('c_login_id'),
            c_password=request.POST.get('c_password'),
            c_email=request.POST.get('c_email'),
            c_contact=request.POST.get('c_contact'),
            c_address=request.POST.get('c_address')
        )

        # after register → go back to home (login modal)
        return redirect('/?registered=1')
    
    return redirect('home')

def customer_profile(request):
    if not request.session.get('customer_id'):
        return redirect('home')

    customer = Customer.objects.get(id=request.session['customer_id'])

    if request.method == 'POST':
        customer.c_fullname = request.POST.get('fullname')
        customer.c_contact = request.POST.get('contact')
        customer.c_address = request.POST.get('address')
        customer.save()

        messages.success(request, "Profile updated successfully")  # ✅ HERE
        return redirect('customer_profile')

    return render(request, 'accounts/customer_profile.html', {
        'customer': customer
    })





# <============= Electrician Login =================>
def electrician_login(request):
    if request.method == 'POST':
        login_id = request.POST.get('login_id')
        password = request.POST.get('password')

        try:
            electrician = Electrician.objects.get(
                e_login_id=login_id,
                e_password=password
            )
            request.session['electrician_id'] = electrician.id
            return redirect('electrician_dashboard')

        except Electrician.DoesNotExist:
            return render(request, 'electrician/electrician_login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'electrician/electrician_login.html')

def electrician_logout(request):
    request.session.pop('electrician_id', None)
    return redirect('electrician_login')







# <============= Admin Login =================>
# admin login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = AdminUser.objects.get(
                a_login_id=username,
                a_password=password
            )
            request.session['admin_id'] = admin.id
            return redirect('admin_dashboard')
        except AdminUser.DoesNotExist:
            return render(request, 'admin/admin_login.html', {
                'error': 'Invalid admin credentials'
            })

    return render(request, 'admin/admin_login.html')
def admin_logout(request):
    request.session.pop('admin_id', None)
    return redirect('admin_login')







