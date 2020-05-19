from django.shortcuts import render, redirect
# from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home/home.html', {'title': 'Home'})

def feature(request):
    return render(request, 'home/feature.html', {'title': 'feature'})

def about(request):
    return render(request, 'home/about.html', {'title': 'About'})

def contact(request):
    return render(request, 'home/contact.html', {'title': 'Contact'})

def login(request):
    return render(request, 'home/login.html', {'title': 'Login'})

def register(request):
    return render(request, 'home/register.html', {'title' : 'Register'})

def javascript(request):
    return render(request, 'home/javascript.html', {'title': 'Javascript'})



# python manage.py runserver