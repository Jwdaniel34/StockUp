from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, UserStockPortfolio, UserStockProfitTracker, SoldStockPortfolio


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.EmailField()

    
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('state','city','phone','date_of_birth', 'photo')


class StockPortfolioForm(forms.ModelForm):
    # user = forms.CharField(disabled=True, label= 'Client')
    symbol = forms.CharField(disabled= True)
    company = forms.CharField(disabled= True)
    sector = forms.CharField(disabled= True)
    pay_type = forms.CharField(disabled=True, label='Pay Type')
    price = forms.FloatField()
    dividends = forms.FloatField(disabled= True)
    n_shares = forms.IntegerField(label='Shares')
    class Meta:
        model = UserStockPortfolio
        fields = ('symbol','company','sector','broker','pay_type', 'dividends', 'price','n_shares')
        # fields = ('n_shares', 'price')

class StockGainForm(forms.ModelForm):
    user = forms.CharField()
    cash_gained =  forms.FloatField()
    roi= forms.FloatField()
    class Meta:
        model = UserStockProfitTracker
        fields = ('user','cash_gained', 'roi')

         

class SoldStockForm(forms.ModelForm):
    # user = forms.CharField(disabled=True, label= 'Client')
    stock_id = forms.IntegerField(disabled=True, label='Order Number')
    symbol = forms.CharField(disabled= True)
    company = forms.CharField(disabled= True)
    sector = forms.CharField(disabled= True)
    broker = forms.CharField(disabled=True, label='Broker')
    pay_type = forms.CharField(disabled=True, label='Pay Type')
    price = forms.FloatField(disabled=True, label='Current Price')
    dividends = forms.FloatField(disabled= True)
    n_shares = forms.IntegerField(disabled = True, label='Shares')
    tot_price = forms.FloatField(disabled=True, label='Total')
    class Meta:
        model = SoldStockPortfolio
        fields = ('stock_id','symbol','company','sector','broker','pay_type', 'dividends', 'price','n_shares', 'tot_price')

