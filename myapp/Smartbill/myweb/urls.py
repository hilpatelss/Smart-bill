from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('billing/', views.billing, name='billing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('invoce/', views.invoice, name='invoice'),
    path('products/', views.products, name='products'),
    path('reports/', views.reports, name='reports'),
    path('sales_history/', views.sales_history, name='sales_history'),
    path('settings/', views.settings, name='settings'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('customers/', views.customers, name='customers'),
]