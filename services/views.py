from django.shortcuts import render
from .models import Service



def service_list(request):
    services = Service.objects.all()
    is_customer_logged_in = 'customer_id' in request.session

    return render(request, 'services/service_list.html', {
        'services': services,
        'is_customer_logged_in': is_customer_logged_in
    })