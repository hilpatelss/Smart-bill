from datetime import datetime, timedelta
from time import strftime
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.shortcuts import render, redirect ,reverse
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login ,logout
from django.http import JsonResponse
from django.contrib import messages
from myweb.models import *
from django.db.models import Sum

def home(request):
    context = {"page":"home"}
    return render(request,'index.html',context)

def about(request):
    context = {"page":"home"}
    return render(request,'about.html',context)

@login_required(login_url="/signin/")
def billing(request):
    inv = Invoice.objects.filter(user = request.user).order_by('-id').first()
    inv_number = int(inv.Inv_number) + 1 if inv else 1
    today = date.today()
    due_date = today + timedelta(int(Formet.objects.filter(user = request.user).first().Inv_due_days))  # Example: due date is 30 days from today
    inv_format = Formet.objects.filter(user = request.user).first().Inv_prefix
    products = Products.objects.filter(user = request.user)
    data = {
        "inv_number": inv_number,
        "today":today ,
        "due_date":due_date,
        "inv_format": inv_format,
        "products": products
    }
    if request.method == "POST":
        Customer_mobile = request.POST.get("Customer_number")
        Customer_name = request.POST.get("Customer_name")
        notes = request.POST.get("notes")
        Inv_bill_date = request.POST.get("Inv_bill_date")
        Inv_due_bill_date= request.POST.get("Inv_due_bill_date")
        Inv_payment_mode = request.POST.get("Inv_payment_mode")
        Product_name = request.POST.getlist("Product_name")
        Product_price = [int(x) for x in request.POST.getlist("Product_price")]
        Product_gst = [float(x) for x in request.POST.getlist("Product_gst")]
        Product_qty = [int(x) for x in request.POST.getlist("Product_qty")]
        Inv_subtotal = float(request.POST.get("Inv_subtotal", 0))
        Inv_gst = float(request.POST.get("Inv_gst", 0))
        Inv_Total = float(request.POST.get("Inv_Total", 0))
        Inv_additional_charges = float(request.POST.get("Inv_additional_charges", 0))
        Inv_discount = float(request.POST.get("Inv_discount", 0))

        if not Customer.objects.filter(user=request.user).filter(Customer_mobile = Customer_mobile).exists():
            # Create new customer
            customer = Customer.objects.create(
            user=request.user,
            Customer_name=Customer_name,
            Customer_mobile=Customer_mobile
            )
            customer.save()
        else:
            # Update existing customer's name if different
            customer = Customer.objects.filter(user=request.user).filter(Customer_mobile = Customer_mobile).first()
            if customer.Customer_name != Customer_name:
                customer.Customer_name = Customer_name
                customer.save()
        invoice = Invoice.objects.create(
            user = request.user,
            Inv_number = inv_number,
            Inv_Total = Inv_Total,
            Inv_subtotal = Inv_subtotal,
            Inv_gst = Inv_gst,
            Inv_discount = Inv_discount,
            Inv_additional_charges = Inv_additional_charges,
            Inv_internal_notes = notes,
            Inv_bill_date = date.strptime(Inv_bill_date, '%Y-%m-%d'),
            Inv_due_bill_date = date.strptime(Inv_due_bill_date, '%Y-%m-%d'),
            Inv_payment_mode = Inv_payment_mode,
            Customer_number = Customer_mobile
        )
        invoice.save()  
        print(Product_name,Product_price,Product_gst,Product_qty)
        if len(Product_name) > 0:
            for i in range(len(Product_name)):
                if i < len(Product_price) and i < len(Product_gst) and i < len(Product_qty):
                    sell = Sells.objects.create(
                        user = request.user,
                        Inv_number = Invoice.objects.filter(user = request.user).filter(Inv_number = inv_number).first(),
                        Product_name = Product_name[i],
                        Product_qty = Product_qty[i],
                        Product_price = Product_price[i],
                        Product_gst = Product_gst[i]
                    )
                    sell.save()
        inv_id = Invoice.objects.filter(user = request.user).filter(Inv_number = inv_number).first().id
        return redirect('invoice', inv_id= inv_id)


    context = {"page":"home", "data": data}
    return render(request,'billing.html',context)

@csrf_protect
@login_required(login_url="/signin/")   
def getcustomer(request):
    if request.method == "POST":
        Customer_mobile = request.POST.get("Customer_mobile")
        print(Customer_mobile)
        customer_name = Customer.objects.filter(user=request.user).filter(Customer_mobile = Customer_mobile).first().Customer_name
        if customer_name:   
            success = customer_name.title() 
        else:
            success = "Customer not found"
        return HttpResponse(success)

@login_required(login_url="/signin/")
def dashboard(request):
    context = {"page":"home"}
    return render(request,'dashboard.html',context)

@login_required(login_url="/signin/")   
def customers(request):
    user = request.user   
    Cust  = Customer.objects.filter(user=user).order_by('-id')
    cust_total = Cust.count()
    cust_revenue = 0
    cust_bills = 0
    for c in Cust:
        c.Customer_name = c.Customer_name.title()
        cust_bills += c.customer_bill_count
        cust_revenue += c.customer_bill_spent
        c.initials = c.Customer_name[0].upper() + c.Customer_name.split(" ")[-1][0].upper()

    Stats = {
        "cust_total": cust_total,
        "cust_revenue": cust_revenue,
        "cust_bills": cust_bills
    }

    context = {"page":"customers", "cust" : Cust , "Stats":Stats }
    return render(request,'customers.html',context)

@csrf_protect
@login_required(login_url="/signin/")   
def editcustomer(request):
    if request.method == "POST":
        Customer_name = request.POST.get("Customer_name")
        Customer_mobile = request.POST.get("Customer_mobile")
        Customer_email = request.POST.get("Customer_email")
        user = request.user
        cust  = Customer.objects.filter(user=user).filter(Customer_mobile = Customer_mobile).first()
        cust.Customer_name = Customer_name
        cust.Customer_mobile = Customer_mobile  
        cust.Customer_email = Customer_email
        cust.save()
        print(Customer_name,Customer_mobile,Customer_email)
        return redirect('/customers/')
        
@csrf_protect
@login_required(login_url="/signin/")   
def addcustomer(request):
    if request.method == "POST":
        user =request.user
        Customer_name = request.POST.get("Customer_name")
        Customer_mobile = request.POST.get("Customer_mobile")
        Customer_email = request.POST.get('Customer_email')
        cust = Customer.objects.create(
            user=user,
            Customer_name=Customer_name,
            Customer_mobile=Customer_mobile,
            Customer_email=Customer_email
        )
        cust.save()
        print(Customer_name,Customer_mobile,Customer_email)
        return redirect('/customers/')
    
@login_required(login_url="/signin/")   
def deletecustomer(request):
    if request.method == "POST":
        User = request.user
        Customer_id = request.POST.get("Customer_id")

        cust = Customer.objects.filter(user=User).filter(id = Customer_id).first()
        if cust:
            cust.delete()

        return redirect('/customers/')
    return redirect('/customers/')
 
@login_required(login_url="/signin/")
def invoice(request, inv_id):
    user = request.user
    inv = Invoice.objects.filter(user = request.user).filter(id = inv_id).first()
    print(inv.Inv_number)
    formet = Formet.objects.filter(user = user).first()
    business = Business.objects.filter(user = user).first()
    customer = Customer.objects.filter(user=user).filter(Customer_mobile = inv.Customer_number).first()
    sells = Sells.objects.filter(user=user).filter(Inv_number = inv)
    for item in sells:
        item.Total = item.Product_price * item.Product_qty * (1 + (item.Product_gst ) / 100) if item.Product_gst != 0 else item.Product_price * item.Product_qty
    data = {
        "Shop_name": business.bizName if business else "",
        "Shop_address": business.full_address if business else "",
        "Shop_phone": business.phone_number if business else "",
        "Shop_Gstin": business.Gstin if business else "",
        "Inv_format": formet.Inv_prefix if formet else "",
        "Inv_number": inv.Inv_number,
        "Inv_status": "Paid" if inv.Inv_due_bill_date <= date.today() else "Pending",
        "Inv_date": inv.Inv_bill_date,
        "Inv_due_date": inv.Inv_due_bill_date,
        "Inv_payment_method": inv.Inv_payment_mode,
        "Inv_payment_status": inv.Inv_due_bill_date <= date.today() and "Paid" or "Pending",
        "Inv_subtotal": inv.Inv_subtotal,
        "Inv_gst": inv.Inv_gst,
        "Inv_discount": inv.Inv_discount,
        "Inv_total": inv.Inv_Total,
        "Customer_name": customer.Customer_name if customer else "",
        "Customer_mobile": customer.Customer_mobile if customer else "",
        "Customer_email": customer.Customer_email if customer else "",
        "sells": sells
    }
    context = {"page":"home", "data": data}
    return render(request,'invoice.html',context)

@login_required(login_url="/signin/")
def products(request):
    User = request.user
    prod = Products.objects.filter(user=User)
    prod_count = prod.count()
    Prod_inStock = 0
    Prod_outStock = 0
    prod_lowStock = 0
    for p in prod:
        p.Product_name = p.Product_name.title()
        if p.Product_stock <= 0:
            p.Product_status = "out-stock"
            p.Product_design = "badge-out"
            Prod_outStock += 1
        elif p.Product_stock < 100:
            p.Product_status = "low-stock"
            p.Product_design = "badge-low"
            prod_lowStock += 1
        else:
            p.Product_status = "in-stock"
            p.Product_design = "badge-in"
            Prod_inStock += 1
    Stats = {
        "prod_count": prod_count,
        "Prod_inStock": Prod_inStock,
        "Prod_outStock": Prod_outStock,
        "prod_lowStock": prod_lowStock
    }
    context = {"page":"home", "prod": prod, "Stats": Stats}
    return render(request,'products.html',context)

@login_required(login_url="/signin/")   
def editproducts(request):
    if request.method == "POST":
        id = request.POST.get("id")
        Name = request.POST.get("Name")
        Price = request.POST.get("Price")
        gst = request.POST.get('gst')
        Stock = request.POST.get('Stock')
        prod = Products.objects.filter(user=request.user).filter(id = id).first()
        prod.Product_name = Name
        prod.Product_price = Price
        prod.Product_gst = gst
        prod.Product_stock = Stock
        prod.save()
        print(id,Name,Price,gst,Stock)
        return redirect('/products/')
    
@csrf_protect
@login_required(login_url="/signin/")   
def addproducts(request):
    if request.method == "POST":
        Name = request.POST.get("Name")
        Price = request.POST.get("Price")
        gst = request.POST.get('gst')
        Stock = request.POST.get('Stock')
        prod = Products.objects.create(
            user = request.user,
            Product_name = Name,
            Product_price = Price,
            Product_stock = Stock,
            Product_gst =gst
        )
        prod.save()
        print(Name,Price,gst,Stock)
        return redirect('/products/')
    
@login_required(login_url="/signin/")   
def deleteproducts(request):
    if request.method == "POST":
        Products_id = request.POST.get("Products_id")
        User = request.user
        prod = Products.objects.filter(user=User).filter(id = Products_id).first()
        if prod:
            prod.delete()
        print(Customer_mobile)
        return redirect('/customers/')
    return redirect('/products/')

@login_required(login_url="/signin/")
def reports(request):
    User = request.user
    invoices = Invoice.objects.filter(user=User)
    total_revenue = sum(inv.Inv_Total for inv in invoices)
    invoices_generated = invoices.count()
    avg_order_value = total_revenue / invoices_generated if invoices_generated > 0 else 0
    total_gst_collected = sum(inv.Inv_GST for inv in invoices)
    invoices = invoices.order_by('-Inv_bill_date')[:5]
    sun = 0  
    mon = 0     
    tue = 0 
    wed = 0
    thu = 0
    fri = 0
    sat = 0
    for inv in invoices:
        if inv.Inv_bill_date.weekday() == 6:
            sun += inv.Inv_Total
        elif inv.Inv_bill_date.weekday() == 0:
            mon += inv.Inv_Total
        elif inv.Inv_bill_date.weekday() == 1:
            tue += inv.Inv_Total
        elif inv.Inv_bill_date.weekday() == 2:
            wed += inv.Inv_Total
        elif inv.Inv_bill_date.weekday() == 3:
            thu += inv.Inv_Total
        elif inv.Inv_bill_date.weekday() == 4:
            fri += inv.Inv_Total
        elif inv.Inv_bill_date.weekday() == 5:
            sat += inv.Inv_Total
    revenue = (max([sun, mon, tue, wed, thu, fri, sat]))
    sun_height = f'{(sun / revenue) * 130 if revenue > 0 else 0 }px'
    mon_height = f'{(mon / revenue) * 130 if revenue > 0 else 0 }px'
    tue_height = f'{(tue / revenue) * 130 if revenue > 0 else 0 }px'
    wed_height = f'{(wed / revenue) * 130 if revenue > 0 else 0 }px'
    thu_height = f'{(thu / revenue) * 130 if revenue > 0 else 0 }px'
    fri_height = f'{(fri / revenue) * 130 if revenue > 0 else 0 }px'
    sat_height = f'{(sat / revenue) * 130 if revenue > 0 else 0 }px'  

    top = {}
    sells = Sells.objects.filter(user=User).annotate(total_qty=Sum('product_qty')).order_by('product_name')
    for sell in sells:
        top[sell.name] = sell.total_qty * sell.Product_price * (1 + (sell.Product_gst / 100))
    top = dict(sorted(top.items(), key=lambda item: item[1], reverse=True)[:5])
    top_1_h = top[list(top.keys())[0]] / sum(top.values()) * 100 if sum(top.values()) > 0 else 0
    top_2_h = top[list(top.keys())[1]] / sum(top.values()) * 100 if sum(top.values()) > 0 else 0
    top_3_h = top[list(top.keys())[2]] / sum(top.values()) * 100 if sum(top.values()) > 0 else 0
    top_4_h = top[list(top.keys())[3]] / sum(top.values()) * 100 if sum(top.values()) > 0 else 0
    top_5_h = top[list(top.keys())[4]] / sum(top.values()) * 100 if sum(top.values()) > 0 else 0    

    data =  { "total_revenue": total_revenue, "invoices_generated": invoices_generated,"avg_order_value": avg_order_value,"total_gst_collected": total_gst_collected,"sun": sun,"mon": mon,"tue": tue,"wed": wed,"thu": thu,"fri": fri,"sat": sat,"sun_height": sun_height,"mon_height": mon_height,"tue_height": tue_height,"wed_height": wed_height,"thu_height": thu_height,"fri_height": fri_height,"sat_height": sat_height ,"top": top,"top_1_h": top_1_h,"top_2_h": top_2_h,"top_3_h": top_3_h,"top_4_h": top_4_h,"top_5_h": top_5_h }
    context = {"page":"home", "data": data}
    return render(request,'reports.html',context)

@login_required(login_url="/signin/")
def sales_history(request):
    user = request.user
    inv = Invoice.objects.filter(user =user)
    total_coll = inv.filter(Inv_due_bill_date= date.today()).aggregate(total=Sum('Inv_Total'))['total'] or 0
    total_pen = inv.filter(Inv_due_bill_date__lte = date.today()).aggregate(total=Sum('Inv_Total'))['total'] or 0
    total_T_rev = inv.filter(Inv_due_bill_date__gte = date.today()).aggregate(total=Sum('Inv_Total'))['total'] or 0
    invoice = inv.order_by('-Inv_bill_date')
    formet = Formet.objects.filter(user = user).first()
    for i in invoice:    
            i.Inv_status = "Paid" if i.Inv_due_bill_date <= date.today() else "Pending"
            i.Customer_name = Customer.objects.filter(user=user).filter(Customer_mobile = i.Customer_number).first().Customer_name
    data = {
        "inv" : invoice,
        "total_inv": inv.count(),
        "total_coll": total_coll,
        "total_pen": total_pen,
        "total_T_rev": total_T_rev,
        "Formet": formet
    }
    context = {"page":"home","data": data}
    return render(request,'sales_history.html',context)

@login_required(login_url="/signin/")
def settings(request): 
    user = request.user
    biz = Business.objects.filter(user = user).first()
    format = Formet.objects.filter(user = user).first()
    context = {"page":"home", "biz": biz, "user": user ,"format":format }
    return render(request,'settings.html',context)

@csrf_protect
@login_required(login_url="/signin/")
def editbiz(request):
    if request.method == "POST":
        bizName = request.POST.get("bizName")
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        full_address = request.POST.get("full_address")
        Gstin = request.POST.get("Gstin")
        Pan_number = request.POST.get("Pan_number")
        user = request.user
        business = Business.objects.filter(user=user).first()
        business.bizName = bizName
        business.full_address = full_address
        business.phone_number = phone_number
        business.Gstin = Gstin
        business.Pan_number = Pan_number
        business.save()
        print(bizName,full_name,phone_number,full_address,Gstin,Pan_number)
    return redirect('/settings/#tab-shop')

@csrf_protect
@login_required(login_url="/signin/")
def editinv(request):
    if request.method == "POST":
        Inv_prefix = request.POST.get("Inv_prefix")
        Inv_footer = request.POST.get("Inv_footer")
        Inv_due_days = request.POST.get("Inv_due_days")
        Show_signature_area = request.POST.get("Show_signature_area")
        Show_TC = request.POST.get("Show_TC")
        user = request.user
        format = Formet.objects.filter(user=user).first()
        format.Inv_prefix = Inv_prefix
        format.Inv_footer = Inv_footer
        format.Inv_due_days = Inv_due_days
        format.Show_signature_area = True if Show_signature_area == "true" else False
        format.Show_TC = True if Show_TC == "true" else False
        format.save()
        print(Inv_prefix,Inv_footer,Inv_due_days,Show_signature_area,Show_TC)
        return redirect(reverse('settings') + '#tab-invoice')

@csrf_protect
@login_required(login_url="/signin/")   
def edituser(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        full_name = request.POST.get("full_name")
        first_name, last_name = full_name.split()
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        if pass2 == "":
            user = request.user
            user.username = username
            user.first_name =first_name
            user.last_name =last_name
            user.save()
        else:
            user = request.user
            user.username = username
            user.first_name =first_name
            user.last_name =last_name
            if user == authenticate(username =username,password =pass1):
                user.set_password(pass2)
            user.save()
            return render('/settings/#tab-account')
        
        return render('/settings/#tab-account')
 
@csrf_protect
def signin(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        print(username,password)
        if not User.objects.filter(username = username).exists():
            messages.info(request, 'invalid Username')
            return redirect('/signin/')
        
        user = authenticate(username =username,password =password)
        
        if user is None:
            messages.info(request, 'invalid password')
            return redirect('/signin/')
        else:
            login(request ,user)
            return redirect('/dashboard/')
    context = {"page":"SignIn"}
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

        formet = Formet.objects.create(
            user =user, 
        )
        formet.save()

        login(request ,user)
        return redirect('/dashboard/')
    context = {"page":"SignUp"}
    return render(request,'signup.html',context)

@login_required(login_url="/signin/")
def Signout(request):
    logout(request)
    return redirect('/signin/')


