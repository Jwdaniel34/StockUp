"""stockup_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from users import views
from .views import StockListView, StockDetailView
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('stockdashboard/', views.stockdashboard, name='stockdashboard'),
    path('ticker/', views.tickersearch, name='ticker'),
    path('userportfolio/', StockListView.as_view(), name='userstockportfolio'),
    path('detailedstock/<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
    path('profile/', views.profile, name= 'profile'),
    path('addstock/', views.addstock, name= 'addstock'),
    path('soldstock/', views.soldstock, name='soldstock'),
    path('register/', views.register, name= 'register'),
    path('edit/', views.edit, name='edit'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name= 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name= 'logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete')
]

urlpatterns += staticfiles_urlpatterns()