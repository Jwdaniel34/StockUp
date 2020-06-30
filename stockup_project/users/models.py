# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class MlDividends(models.Model):
    symbol = models.TextField(blank=True, null=False, primary_key= True)
    company = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    pay_type = models.TextField(blank=True, null=True)
    load_date = models.DateField(blank=True, null=True)
    prevclose = models.FloatField(blank=True, null=True)
    targetprice = models.FloatField(blank=True, null=True)
    orders = models.TextField(blank=True, null=True)
    dividend = models.FloatField(blank=True, null=True)
    increased = models.FloatField(blank=True, null=True)
    payment_date = models.TextField(blank=True, null=True)
    payout = models.FloatField(blank=True, null=True)
    dividendyield = models.FloatField(blank=True, null=True)
    p_e = models.FloatField(blank=True, null=True)
    growth_pe = models.BigIntegerField(blank=True, null=True)
    good_div = models.BigIntegerField(blank=True, null=True)
    healthy_div = models.BigIntegerField(blank=True, null=True)
    highrisk_div = models.BigIntegerField(blank=True, null=True)
    bad_div = models.BigIntegerField(blank=True, null=True)
    basic_materials = models.BigIntegerField(db_column='Basic Materials', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    conglomerates = models.BigIntegerField(db_column='Conglomerates', blank=True, null=True)  # Field name made lowercase.
    consumer_goods = models.BigIntegerField(db_column='Consumer Goods', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    financial = models.BigIntegerField(db_column='Financial', blank=True, null=True)  # Field name made lowercase.
    healthcare = models.BigIntegerField(db_column='Healthcare', blank=True, null=True)  # Field name made lowercase.
    industrial_goods = models.BigIntegerField(db_column='Industrial Goods', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    services = models.BigIntegerField(db_column='Services', blank=True, null=True)  # Field name made lowercase.
    technology = models.BigIntegerField(db_column='Technology', blank=True, null=True)  # Field name made lowercase.
    utilities = models.BigIntegerField(db_column='Utilities', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ML_DIVIDENDS'


class TechnicalDivs(models.Model):
    symbol = models.TextField(blank=True, null=True)
    number_52wlow = models.TextField(db_column='52wlow', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_52whigh = models.TextField(db_column='52whigh', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    perfquarter = models.TextField(blank=True, null=True)
    perfhalfy = models.TextField(blank=True, null=True)
    perfmonth = models.TextField(blank=True, null=True)
    perfweek = models.TextField(blank=True, null=True)
    perfyear = models.TextField(blank=True, null=True)
    perfytd = models.TextField(blank=True, null=True)
    prevclose = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    targetprice = models.TextField(blank=True, null=True)
    atr = models.TextField(blank=True, null=True)
    rsi = models.TextField(blank=True, null=True)
    volatility = models.TextField(blank=True, null=True)
    optionable = models.TextField(blank=True, null=True)
    relvolume = models.TextField(blank=True, null=True)
    shortable = models.TextField(blank=True, null=True)
    payout = models.TextField(blank=True, null=True)
    avgvolume = models.FloatField(blank=True, null=True)
    recom = models.TextField(blank=True, null=True)
    sma20 = models.TextField(blank=True, null=True)
    sma50 = models.TextField(blank=True, null=True)
    sma200 = models.TextField(blank=True, null=True)
    volume = models.TextField(blank=True, null=True)
    change = models.TextField(blank=True, null=True)
    beta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TECHNICAL_DIVS'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to= 'users/%Y/%m/%d/',null=True, blank=True,)

    def __str__(self):
        return f'Profile for user {self.user.username}'

                    



# class UserStockPortfolio(models.Model):
    # name = models.ForeignKey(Users, on_delete=SET_NULL)
    # symbol = models.CharField(max_length=200, null=True)
    # sector = models.CharField(max_length=200, null=True)
    # price = models.FloatFiield(null=True)
    # dividends = models.FloatFiield(null=True)
    # n_shares = models.IntField(null= True)
    # date_created = models.DateTimeField(auto_now_add=True, null = True)


# class UserStockProfitTracker(models.Model):
    # name = models.ForeignKey(Users, on_delete=SET_NULL)
    # cash_amount =  models.FloatFiield(null=True) 
    # date_created = models.DateTimeField(auto_now_add=True, null = True)
