from django.shortcuts import render

#home view
def home(request):
    return render(request, 'home.html')

#about view
def about(request):
    return render(request, 'about.html')


