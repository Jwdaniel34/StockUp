from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.

post = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post cotent',
        'date_posted': 'August 27, 2018',
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'First post cotent',
        'date_posted': 'August 27, 2018',
    } 
]

def home(request):
    context = {
        'posts': post
    }
    return render(request, 'home/home.html', context, {'title': 'Home'})

def feature(request):
    context = {
        'posts': post
    }
    return render(request, 'home/feature.html', context, {'title': 'feature'})


def about(request):
    return render(request, 'home/about.html', {'title': 'About'})

def contact(request):
    return render(request, 'home/contact.html', {'title': 'Contact'})


def javascript(request):
    return render(request, 'home/javascript.html', {'title': 'Javascript'})


    # python manage.py runserver