from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (UserRegisterForm, UserEditForm,
                    ProfileEditForm, StockPortfolioForm,
                    StockGainForm, SoldStockForm)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .models import (MlDividends, Profile, UserStockPortfolio, 
                    UserStockProfitTracker, SoldStockPortfolio)
from django.db.models import Sum, Count
from datetime import datetime, timedelta
import json
import requests
from django.utils import timezone
from django_q.tasks import async_task
import os 

iex = os.environ.get('IEX_KEY')

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



    pl = sp.aggregate(Sum('tot_price'))
    div = sp.values('dividends')
    payT = sp.values('pay_type')
    shares = sp.values('n_shares')
    tot_div = []
    pO = []

    for pay, ty, current, share, sym in zip(div,payT, sp.values('purchased'),shares, sp.values('symbol')):
        pay = pay.get('dividends')
        current = current.get('purchased')
        ty = ty.get('pay_type')
        share = share.get('n_shares')
        sym = sym.get('symbol')

        if ty == 'Quarterly' and current == 'Current':
            quart = 4 * pay
            quart = quart * share
            tot_div.append(quart)
        elif ty =='Monthly' and current == 'Current':
            month = 12 * pay
            month = month * share
            tot_div.append(month)
        elif ty == 'Semi-Annual' and current == 'Current':
            semi = 2 * pay
            semi = semi * share
            tot_div.append(semi)
        elif ty == 'Annual' and current == 'Current':
            annual = 1 * pay
            annual = annual * share 
            tot_div.append(annual)


    for sym, share ,current,cp in zip(sp.values('symbol'), shares, sp.values('purchased'), sp.values('id')):
        current = current.get('purchased')
        sym = sym.get('symbol').lower()
        cp = cp.get('id')
        share = share.get('n_shares')
        if current == 'Current': 
            api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{sym}/quote?token={iex}")
            price = json.loads(api_request.content)
            price = price.get('latestPrice')
            pO.append(float(price) * share )
        else:
            sold_stock = SoldStockPortfolio.objects.get(stock_id=cp)
            sold_price = SoldStockPortfolio.objects.filter(stock_id=cp).values()
            sold_price = [ SP['tot_price'] for SP in list(sold_price.values('tot_price'))]
            sold_price = sold_price[0]
            pO.append(sold_price)


    pl = pl.get('tot_price__sum') # Initial Price
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
    ts_price = []
    ts_dates = []

    timeseries_symbol = UserStockProfitTracker.objects.values('cash_gained','date_created')
    for tsstocks in timeseries_symbol:
        cash = float(tsstocks['cash_gained'])
        ts_price.append("{:.2f}".format(cash))
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
        'ts_price': ts_price,
        'ts_dates': ts_dates,
        'tickersymbols': tickersymbols,
        'cash_gained': cashGained,
        'd': d,
        'roi': roi,
    }

    return render(request, 'users/skeleton.html', context )

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
        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker.lower()}/quote?token={iex}")
        api_company = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker.lower()}/company?token={iex}")
        api_dividend = requests.get(f"https://cloud.iexapis.com/stable/data-points/{ticker.lower()}/LAST-DIVIDEND-AMOUNT?token={iex}")
        api_divType= requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker.lower()}/dividends/ytd?token={iex}")


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
    Barlabels = []
    Bardata = []
    my_p = Profile.objects.get(user=request.user)
    sp = UserStockPortfolio.objects.filter(user__user__username=my_p)


    pl = sp.aggregate(Sum('tot_price'))
    div = sp.values('dividends')
    payT = sp.values('pay_type')
    shares = sp.values('n_shares')
    tot_div = []
    pO = []
    
    for pay, ty, current, share, sym in zip(div,payT, sp.values('purchased'),shares, sp.values('symbol')):
        pay = pay.get('dividends')
        current = current.get('purchased')
        ty = ty.get('pay_type')
        share = share.get('n_shares')
        sym = sym.get('symbol')

        if ty == 'Quarterly' and current == 'Current':
            quart = 4 * pay
            quart = quart * share
            tot_div.append(quart)
        elif ty =='Monthly' and current == 'Current':
            month = 12 * pay
            month = month * share
            tot_div.append(month)
        elif ty == 'Semi-Annual' and current == 'Current':
            semi = 2 * pay
            semi = semi * share
            tot_div.append(semi)
        elif ty == 'Annual' and current == 'Current':
            annual = 1 * pay
            annual = annual * share 
            tot_div.append(annual)


    for sym, share ,current,cp in zip(sp.values('symbol'), shares, sp.values('purchased'), sp.values('id')):
        current = current.get('purchased')
        sym = sym.get('symbol').lower()
        cp = cp.get('id')
        share = share.get('n_shares')
        if current == 'Current': 
            api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{sym}/quote?token={iex}")
            price = json.loads(api_request.content)
            price = price.get('latestPrice')
            pO.append(float(price) * share )
        else:
            sold_stock = SoldStockPortfolio.objects.get(stock_id=cp)
            sold_price = SoldStockPortfolio.objects.filter(stock_id=cp).values()
            sold_price = [ SP['tot_price'] for SP in list(sold_price.values('tot_price'))]
            sold_price = sold_price[0]
            pO.append(sold_price)


    pl = pl.get('tot_price__sum') # Initial Price
    pO = sum(pO) # Current Price
    d = sum(tot_div) # Dividends
    cashGained = (pO-pl)+d/pO
    roi = cashGained/pl * 1

    #Query by sector overview
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
    ts_price = []
    ts_dates = []

    timeseries_symbol = UserStockProfitTracker.objects.values('cash_gained','date_created')
    for tsstocks in timeseries_symbol:
        cash = float(tsstocks['cash_gained'])
        ts_price.append("{:.2f}".format(cash))
        ts_dates.append(tsstocks['date_created'].strftime("%Y-%m-%d"))

    tickersymbol = MlDividends.objects.order_by(
                                        "symbol").values('symbol', 'company').distinct().using('dividend')
    tickersymbols = []

    for ticks in tickersymbol:
        sym = f"{ticks['symbol']} - {ticks['company']}"
        tickersymbols.append(sym)

    
    context = {
        'Bardata': Bardata,
        'Barlabels': list(labelsColors.keys()),
        'colors': list(labelsColors.values()),
        'zippedLC': zippedLC,
        'ts_price': ts_price,
        'ts_dates': ts_dates,
        'tickersymbols': tickersymbols,
        'ann_div': d,
        'cash_gained': cashGained,
        'roi': roi,
    }

    
    return render(request, 'users/profile.html', context)



def userportfolio(request):
    my_p = Profile.objects.get(user=request.user)
    sp = UserStockPortfolio.objects.filter(user__user__username=my_p)
    quick_math = 3-5

    context = {'math': quick_math}

    return render(request, 'users/addedportofolio.html', context)


class StockListView(LoginRequiredMixin, ListView):
    model = UserStockPortfolio
    template_name = 'users/addedportofolio.html'
    context_object_name='portfolio'
    ordering = ['company']




class StockDetailView(LoginRequiredMixin,DetailView):
    model = UserStockPortfolio

    def get_context_data(self, **kwargs):
        context = super(StockDetailView, self).get_context_data(**kwargs)
        self.request.session['company'] = self.object.company
        self.request.session['symbol'] = self.object.symbol
        self.request.session['sectors'] = self.object.sector
        self.request.session['brokers'] = self.object.broker
        self.request.session['n_shares'] = self.object.n_shares
        self.request.session['dividends'] = self.object.dividends
        self.request.session['pay_type'] = self.object.pay_type
        self.request.session['tot_price'] = self.object.tot_price
        self.request.session['id'] = self.object.pk
        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{self.object.symbol}/quote?token={iex}")
        price = json.loads(api_request.content)
        context['lastprice'] = price.get('latestPrice')
        try:
            sold_stock = SoldStockPortfolio.objects.get(stock_id=self.object.pk)
            sold_price = SoldStockPortfolio.objects.filter(stock_id=self.object.pk).values()
            sold_date = [ SP['date_created'] for SP in list(sold_price.values('date_created'))]
            sold_price = [ SP['tot_price'] for SP in list(sold_price.values('tot_price'))]
            sold_price = sold_price[0]
            sold_date = sold_date[0].strftime("%m/%d/%Y")
            context['sold'] = sold_stock
            context['dates'] = sold_date
            context['gain'] = sold_price - self.object.tot_price
        except SoldStockPortfolio.DoesNotExist:
            None
        return context

@login_required
def soldstock(request):
    company = request.session['company']
    symbol = request.session['symbol']            
    sector = request.session['sectors'] 
    broker = request.session['brokers']
    dividend = request.session['dividends']
    shares = request.session['n_shares']
    payType = request.session['pay_type']
    prev_tot = request.session['tot_price']
    stock_id = request.session['id']

    api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={iex}")
    price = json.loads(api_request.content)
    price = price.get('latestPrice')
    total_price = price * shares
    gain = total_price - prev_tot

    data = { 
        'stock_id': stock_id,
        'symbol': symbol, 
        'company': company,
        'sector': sector,
        'price' : price,
        'broker': broker,
        'n_shares': shares,
        'pay_type': payType.title(),
        'dividends': dividend,
        'tot_price': total_price,
        }

    current_stock = UserStockPortfolio.objects.get(pk = stock_id)
    stock_form = SoldStockForm(request.POST or None, initial=data)
    
    if stock_form.is_valid():
        stock_form.save(commit=False)
        my_p = Profile.objects.get(user=request.user)
        stock_form.instance.user = my_p
        current_stock.purchased = 'Sold'
        stock_form.save()
        current_stock.save()
        messages.success(request, 'Stock Sold '\
                                        'successfully')
        return redirect ('stock-detail', pk = stock_id)


    stockForm = {
        'sellstockform': stock_form,
        'symbol': symbol,
        'company': company,
        'gain': gain,
        'dividend': dividend,
        'id': stock_id
    }

    return render(request, 'users/soldstocks.html', stockForm)