from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login ,logout
from django.contrib import messages
from myweb.models import *

def home(request):
    context = {"page":"home"}
    return render(request,'index.html',context)

def about(request):
    context = {"page":"home"}
    return render(request,'about.html',context)

@login_required(login_url="/signin/")
def billing(request):
    context = {"page":"home"}
    return render(request,'billing.html',context)

@login_required(login_url="/signin/")
def dashboard(request):
    context = {"page":"home"}
    return render(request,'dashboard.html',context)

@login_required(login_url="/signin/")
def editbiz(request):
    if request.method == "POST":
        bizName = request.POST.get(bizName)
        full_name = request.POST.get(full_name)
        phone_number = request.POST.get(phone_number)
        full_address = request.POST.get(full_address)
        Gstin = request.POST.get(Gstin)
        Pan_number = request.POST.get(Pan_number)
    return redirect('/settings/#tab-shop')

@login_required(login_url="/signin/")
def editinv(request):
    if request.method == "POST":
        Inv_prefix = request.POST.get(Inv_prefix)
        Inv_footer = request.POST.get(Inv_footer)
        Inv_due_days = request.POST.get(Inv_due_days)
        Show_signature_area = request.POST.get(Show_signature_area)
        Show_TC = request.POST.get(Show_TC)
        return redirect('/settings/#tab-invoice')

@login_required(login_url="/signin/")   
def edituser(request):
    if request.method == "POST":
        username = request.POST.get(username)
        full_name = request.POST.get(full_name)
        pass1 = request.POST.get(pass1)
        pass2 = request.POST.get(pass2)
        pass3 = request.POST.get(pass3)
        return redirect('/settings/#tab-account')
 
@login_required(login_url="/signin/")   
def editcustomer(request):
    if request.method == "POST":
        Customer_name = request.POST.get(Customer_name)
        Customer_mobile = request.POST.get(Customer_mobile)
        Customer_email = request.POST.get(Customer_email)
        return redirect('/settings/#tab-account')

@login_required(login_url="/signin/")   
def addcustomer(request):
    if request.method == "POST":
        Customer_name = request.POST.get(Customer_name)
        Customer_mobile = request.POST.get(Customer_mobile)
        Customer_email = request.POST.get(Customer_email)
        return redirect('/settings/#tab-account')
 
@login_required(login_url="/signin/")
def invoice(request):
    context = {"page":"home"}
    return render(request,'invoice.html',context)

@login_required(login_url="/signin/")
def products(request):
    context = {"page":"home"}
    return render(request,'products.html',context)

@login_required(login_url="/signin/")
def reports(request):
    context = {"page":"home"}
    return render(request,'reports.html',context)

@login_required(login_url="/signin/")
def sales_history(request):
    context = {"page":"home"}
    return render(request,'sales_history.html',context)

@login_required(login_url="/signin/")
def settings(request):
    context = {"page":"home"}
    return render(request,'settings.html',context)

@csrf_protect
def signin(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request, 'invalid Username')
            return redirect('/signin/')
        
        user = authenticate(username =username,password =password)
        
        if User is None:
            messages.info(request, 'invalid password')
            return redirect('/signin/')
        else:
            login(request ,user)
            return redirect('/dashboard/')
    context = {"page":"home"}
    return render(request,'signin.html',context)

@csrf_protect
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name") 
        last_name = request.POST.get("last_name") 
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone_number = request.POST.get("phone_number")
        bizName = request.POST.get("bizName")
        bizType = request.POST.get("bizType")
        Gstin = request.POST.get("Gstin")
        City = request.POST.get("City")

        user= User.objects.filter(username = username)
        if  user.exists() :
            messages.info(request, 'username is alraedy register')
            return redirect('/signup/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()
         
        if len(Gstin) == 0:
            Gstin ="A" 

        business = Business.objects.create(
            user =user, 
            phone_number = phone_number,
            bizName = bizName,
            bizType = bizType,
            Gstin = Gstin,
            City = City
        )
        business.save()

        login(request ,user)
        return redirect('dashboard')
    context = {"page":"home"}
    return render(request,'signup.html',context)

@login_required(login_url="/signin/")
def signout(request):
    logout(request)
    return redirect('/signup/')

def customers(request):
    context = {"page":"home"}
    return render(request,'customers.html',context)

