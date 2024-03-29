from django.contrib import admin
from .models import MlDividends
from .models import Profile
from .models import UserStockPortfolio,UserStockProfitTracker,SoldStockPortfolio

# Register your models here.'

admin.site.register(MlDividends)
admin.site.register(UserStockPortfolio)
admin.site.register(UserStockProfitTracker)
admin.site.register(SoldStockPortfolio)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

