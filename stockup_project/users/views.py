from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MlDividends
from django.db.models import Sum, Count
from datetime import datetime, timedelta
import json
# Create your views here.

def register(request):
    if request.method == 'POST':
          form = UserRegisterForm(request.POST)
          if form.is_valid():
              form.save()
              username = form.cleaned_data.get('username')
              messages.success(request, f'Your account has been created! You are now able to log in')
              return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def stockdashboard(request):
    Barlabels = []
    Bardata = []
    today = datetime.now()
    yesterday = datetime.today() - timedelta(days=0)
    # Daily Price action
    div = MlDividends.objects.filter(load_date__month= yesterday.month, load_date__day = yesterday.day).using('dividend')
    if div.exists():
        div = MlDividends.objects.filter(load_date__month= yesterday.month, load_date__day = yesterday.day).using('dividend')
    else:
        yesterday = datetime.today() - timedelta(days=1)
        div = MlDividends.objects.filter(load_date__month= yesterday.month, load_date__day = yesterday.day).using('dividend')

    # Dashboard Chart
    queryset = div.values('sector').annotate(sector_count=Count('sector'))
    for stocks in queryset:
        Barlabels.append(stocks['sector'])
        Bardata.append(stocks['sector_count'])
    
    colors =  [
                      'rgba(54, 162, 235, 0.2)', # Conglomerates
                      'rgba(145, 71, 218, 0.67)', # Consumer Goods 
                      'rgba(255, 206, 86, 0.2)', # Technology 
                      'rgba(33, 122, 211, 0.67)', # Industrial Goods
                      'rgba(153, 102, 255, 0.2)', # Utilities
                      'rgba(218, 145, 71, 0.67)', # Basic Material
                      'rgb(71, 218, 71, 0.2)', # Services
                      'rgba(218, 71, 145, 0.74)', # Financial
                      'rgba(255, 99, 132, 0.2)', # Healthcare
                  ]

    labelsColors = dict(zip(Barlabels, colors))
    zippedLC = [(Barlabels, colors)]
    context = {
        "data": div,
        'Bardata': Bardata,
        'Barlabels': list(labelsColors.keys()),
        'colors': list(labelsColors.values()),
        'zippedLC': zippedLC,
    }

    return render(request, 'users/stockdashboard.html', context )




@login_required
def profile(request):
    return render(request, 'users/profile.html')

