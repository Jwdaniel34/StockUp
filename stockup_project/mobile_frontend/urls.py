from django.urls import path
from . import views


urlpatterns = [
    path('mobile/', views.index)
]