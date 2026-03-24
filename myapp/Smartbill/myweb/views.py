from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate ,login ,logout
from django.contrib import messages
from myweb.models import *

def home(request):
    context = {"page":"home"}
    return render(request,'index.html',context)

def about(request):
    context = {"page":"home"}
    return render(request,'about.html',context)

def billing(request):
    context = {"page":"home"}
    return render(request,'billing.html',context)

def dashboard(request):
    context = {"page":"home"}
    return render(request,'dashboard.html',context)

def forget_password(request):
    context = {"page":"home"}
    return render(request,'forget_password.html',context)

def invoice(request):
    context = {"page":"home"}
    return render(request,'invoice.html',context)

def products(request):
    context = {"page":"home"}
    return render(request,'products.html',context)

def reports(request):
    context = {"page":"home"}
    return render(request,'reports.html',context)

def sales_history(request):
    context = {"page":"home"}
    return render(request,'sales_history.html',context)

def settings(request):
    context = {"page":"home"}
    return render(request,'settings.html',context)

def signin(request):
    context = {"page":"home"}
    return render(request,'signin.html',context)

def signup(request):
    context = {"page":"home"}
    return render(request,'signup.html',context)

def customers(request):
    context = {"page":"home"}
    return render(request,'customers.html',context)

