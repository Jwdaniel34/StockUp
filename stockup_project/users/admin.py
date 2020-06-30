from django.contrib import admin
from .models import MlDividends
from .models import Profile

# Register your models here.'

admin.site.register(MlDividends)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

