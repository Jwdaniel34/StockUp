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
import requests
from django.utils import timezone
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
    today = timezone.now()  - timedelta(days=1)
    # Daily Price action
    div = MlDividends.objects.filter(load_date__month= today.month, load_date__day = today.day).using('dividend')
    if div.exists():
        div = MlDividends.objects.filter(load_date__month= today.month, load_date__day = today.day).using('dividend')
    else:
        yesterday = timezone.now() - timedelta(days=2) 
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

     #Timeseries Chart
    timeseries = MlDividends.objects.using('dividend')
    timeseries_symbol = MlDividends.objects.filter(
                                symbol= "A",).values('prevclose','load_date').using('dividend')
    ts_price = []
    ts_dates = []
    for tsstocks in timeseries_symbol:
        ts_price.append(float(tsstocks['prevclose']))
        ts_dates.append(tsstocks['load_date'])

    context = {
        "data": div,
        'Bardata': Bardata,
        'Barlabels': list(labelsColors.keys()),
        'colors': list(labelsColors.values()),
        'zippedLC': zippedLC,
        'ts_price': ts_price,
        'ts_dates': ts_dates,
    }

    return render(request, 'users/stockdashboard.html', context )

def tickersearch(request):
    # pk_7b4f56cf15be4f548126330ab143502c 
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker.lower()}/quote?token=pk_7b4f56cf15be4f548126330ab143502c")
        
        try:
            api = json.loads(api_request.content)
            context = {'api': api
            }
            return render(request, 'users/ticker.html', context)
        except Exception as e:
            api = "Error..."
            context = {'api': api
            }
            return render(request, 'users/ticker.html', context)
    else: 
        search = { 'tickers': "Enter a Ticker Symbol Above..."
        }
        return render(request, 'users/ticker.html', search)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

