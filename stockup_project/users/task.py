from .forms import StockGainForm
from .models import UserStockProfitTracker, Profile,UserStockPortfolio
from django_q.tasks import schedule
from django.contrib.auth.models import User
import requests
from django.db.models import Sum, Count
from datetime import datetime, timedelta
import json

# Schedule.objects.create(func='users.task.cashUpdate',
#                         hook='hooks.print_result',
#                         schedule_type=Schedule.CRON,
#                         cron = '0 09 * * 1-5')


def cashUpdate():
    my_p = Profile.objects.all()
    for users in my_p:
        print('it worked')
        sp = UserStockPortfolio.objects.filter(user__user__username=users)
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
        print(cashGained)
        roi = cashGained/pl * 1

        # information = {
        #     'user': users,
        #     'cashGained':cashGained,
        #     'roi': roi,
        # }
        # print(information)

        UserStockProfitTracker.objects.create(user=users, cash_gained=cashGained,
                                                    roi=roi)
        # form.save(force_insert=True)

