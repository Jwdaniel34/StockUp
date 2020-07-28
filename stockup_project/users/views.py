from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserEditForm, ProfileEditForm, StockPortfolioForm, StockGainForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MlDividends, Profile, UserStockPortfolio, UserStockProfitTracker
from django.db.models import Sum, Count
from datetime import datetime, timedelta
import json
import requests
from django.utils import timezone
from django_q.tasks import async_task

# Create your views here.




# registration for new user
def register(request):
    if request.method == 'POST':
          form = UserRegisterForm(request.POST)
          if form.is_valid():
              form.save()
              Profile.objects.create(user=form)
              username = form.cleaned_data.get('username')
              messages.success(request, f'Your account has been created! You are now able to log in')
              return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


# User edit profile
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
                                instance=request.user,
                                data= request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files= request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                        'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)

    contextEdit = {
        'user_form': user_form,
        'profile_form': profile_form
    } 
    return render(request, 'users/edit.html', contextEdit)


# User Dashboard
@login_required
def stockdashboard(request):
    Barlabels = []
    Bardata = []
    today = timezone.now() - timedelta(days=1)
    # Daily Price action
    table = MlDividends.objects.filter(load_date__month= today.month, load_date__day = today.day).using('dividend')
    if table.exists():
        table = MlDividends.objects.filter(load_date__month= today.month, load_date__day = today.day).using('dividend')
    else:
        yesterday = timezone.now() - timedelta(days=2) 
        table = MlDividends.objects.filter(load_date__month= yesterday.month, load_date__day = yesterday.day).using('dividend')


    # Dashboard Chart
    my_p = Profile.objects.get(user=request.user)
    sp = UserStockPortfolio.objects.filter(user__user__username=my_p)



    pl = sp.aggregate(Sum('price'))
    div = sp.values('dividends')
    payT = sp.values('pay_type')
    tot_div = []
    pO = []
    
    
    for pay, ty in zip(div,payT):
        pay = pay.get('dividends')
        ty = ty.get('pay_type')

        if ty == 'Quarterly':
            quart = 4 * pay
            tot_div.append(quart)
        elif ty =='Monthly':
            month = 12 * pay
            tot_div.append(month)
        elif ty == 'Semi-Annual':
            semi = 2 * pay
            tot_div.append(semi)
        else:
            annual = 1 * pay
            tot_div.append(annual)


    for sym in sp.values('symbol'):
        sym = sym.get('symbol').lower()
        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{sym}/quote?token=pk_7b4f56cf15be4f548126330ab143502c")
        price = json.loads(api_request.content)
        price = price.get('latestPrice')
        pO.append(int(price))

    pl = pl.get('price__sum') # Initial Price
    pO = sum(pO) # Current Price
    d = sum(tot_div) # Dividends
    cashGained = (pO-pl)+d/pO
    roi = cashGained/pl * 1
    informatoin = {
        'cashGained':cashGained,
        'roi': roi,
    }


    queryset = sp.values('sector').annotate(sector_count=Count('sector'))
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
    # timeseries_symbol = MlDividends.objects.filter(symbol='A').values('prevclose','load_date').using('dividend')
    ts_price = []
    ts_dates = []
    # for tsstocks in timeseries_symbol:
    #     ts_price.append(float(tsstocks['prevclose']))
    #     ts_dates.append(tsstocks['load_date'].strftime("%Y-%m-%d"))
    timeseries_symbol = UserStockProfitTracker.objects.values('cash_gained','date_created')
    for tsstocks in timeseries_symbol:
        ts_price.append(float(tsstocks['cash_gained']))
        ts_dates.append(tsstocks['date_created'].strftime("%Y-%m-%d"))


    tickersymbol = MlDividends.objects.order_by(
                                        "symbol").values('symbol', 'company').distinct().using('dividend')
    tickersymbols = []

    for ticks in tickersymbol:
        sym = f"{ticks['symbol']} - {ticks['company']}"
        tickersymbols.append(sym)

    
    context = {
        "data": table,
        'Bardata': Bardata,
        'Barlabels': list(labelsColors.keys()),
        'colors': list(labelsColors.values()),
        'zippedLC': zippedLC,
        'ts_price': ts_price[:2],
        'ts_dates': ts_dates[:2],
        'tickersymbols': tickersymbols,
        'ann_div': d,
        'cash_gained': cashGained,
        'roi': roi,
    }

    return render(request, 'users/stockdashboard.html', context )

@login_required
def tickersearch(request):
    # pk_7b4f56cf15be4f548126330ab143502c
    ticker_company = None
    ticker_dividend = None
    import re
    tickersymbol = MlDividends.objects.order_by(
                                        "symbol").values('symbol', 'company').distinct().using('dividend')
    tickersymbols = []
    for ticks in tickersymbol:
        sym = f"{ticks['symbol']} - {ticks['company']}"
        tickersymbols.append(sym)

    if request.POST.get('ticker'):
        ticker = request.POST.get('ticker')
        ticker = ticker.split("-")
        ticker = ticker[0].replace(" ","")
        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker.lower()}/quote?token=pk_7b4f56cf15be4f548126330ab143502c")
        api_company = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker.lower()}/company?token=pk_7b4f56cf15be4f548126330ab143502c")
        api_dividend = requests.get(f"https://cloud.iexapis.com/stable/data-points/{ticker.lower()}/LAST-DIVIDEND-AMOUNT?token=pk_7b4f56cf15be4f548126330ab143502c")
        api_divType= requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker.lower()}/dividends/ytd?token=pk_7b4f56cf15be4f548126330ab143502c")


        try:
            api = json.loads(api_request.content)
            ticker_company = json.loads(api_company.content)
            ticker_dividend = json.loads(api_dividend.content) 
            dividend_type = json.loads(api_divType.content)
            request.session['symbol'] = api.get('symbol')
            request.session['companyname'] = api.get('companyName')
            request.session['sector'] = ticker_company.get('sector')
            request.session['dividend'] = ticker_dividend
            request.session['paytype'] = dividend_type[0].get('frequency')



            context = {
                'tickersymbols': tickersymbols,
                'api': api,
                'ticker_company': ticker_company,
                'ticker_dividend': ticker_dividend,
                'div_type': dividend_type[0]
            }
            return render(request, 'users/ticker.html', context)

        except Exception as e:
            api = "Error.."
            context = {
                'tickersymbols': tickersymbols,
                'api': api,
                'ticker_company': ticker_company,
                'ticker_dividend': ticker_dividend,
            }
            return render(request, 'users/ticker.html', context)
        
    else:
        search = { 'tickers': "Enter a Ticker Symbol Above...",
                'tickersymbols': tickersymbols
        }

        return render(request, 'users/ticker.html', search)

@login_required
def addstock(request):
    symbol = request.session['symbol']            
    companyName = request.session['companyname'] 
    sector = request.session['sector'] 
    dividend = request.session['dividend'] 
    payType = request.session['paytype']
    # UserStockPortfolio.objects.all().delete()
    print(dividend,payType)
    data = { 
        'symbol': symbol, 
        'company': companyName,
        'sector': sector,
        'pay_type': payType,
        'dividends': dividend }

    stock_form = StockPortfolioForm(request.POST or None, initial=data)
    
    if stock_form.is_valid():
        stock_form.save(commit=False)
        my_p = Profile.objects.get(user=request.user)
        stock_form.instance.user = my_p
        stock_form.save()
        messages.success(request, 'Stock added '\
                                        'successfully')
        return redirect ('ticker')


    stockForm = {
        'stockform': stock_form,
        'symbol': symbol
    }

    return render(request, 'users/addstock.html', stockForm)

@login_required
def profile(request):

    my_p = Profile.objects.get(user=request.user)
    sp = UserStockPortfolio.objects.filter(user__user__username=my_p)


    pl = sp.aggregate(Sum('price'))
    div = sp.values('dividends')
    payT = sp.values('pay_type')
    tot_div = []
    pO = []

    for pay, ty in zip(div,payT):
        pay = pay.get('dividends')
        ty = ty.get('pay_type')

        if ty == 'Quarterly':
            quart = 4 * pay
            tot_div.append(quart)
        elif ty =='Monthly':
            month = 12 * pay
            tot_div.append(month)
        elif ty == 'Semi-Annual':
            semi = 2 * pay
            tot_div.append(semi)
        else:
            annual = 1 * pay
            tot_div.append(annual)


    for sym in sp.values('symbol'):
        sym = sym.get('symbol').lower()
        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{sym}/quote?token=pk_7b4f56cf15be4f548126330ab143502c")
        price = json.loads(api_request.content)
        price = price.get('latestPrice')
        pO.append(int(price))

    pl = pl.get('price__sum') # Initial Price
    pO = sum(pO) # Current Price
    d = sum(tot_div) # Dividends
    cashGained = (pO-pl)+d/pO
    roi = cashGained/pl * 1
    informatoin = {
        'cashGained':cashGained,
        'roi': roi,
    }

    tickersymbol = MlDividends.objects.order_by(
                                        "symbol").values('symbol', 'company').distinct().using('dividend')
    tickersymbols = []

    for ticks in tickersymbol:
        sym = f"{ticks['symbol']} - {ticks['company']}"
        tickersymbols.append(sym)
    
    context = {
        'tickersymbols': tickersymbols,
        'cash_gained': cashGained,
    }
    
    return render(request, 'users/profile.html', context)


    
# now = datetime.now()
# date= datetime(year= now.year, month= now.month, day= now.day, hour= 17,minute= 0)
# cashUpdate(schedule= date,repeat=Task.DAILY, information=informatoin)
    
    