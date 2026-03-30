from django.db import models
from django.contrib.auth.models import  User
# Create your models here.

class Business(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number =models.IntegerField(max_length=10)
    bizName = models.CharField(max_length=255)
    bizType = models.CharField(max_length=255)
    Gstin = models.CharField(default="")
    City = models.CharField(max_length=255)
    full_address = models.TextField(default="")
    Pan_number =models.CharField(default="",max_length=15)
    shop_logo = models.ImageField(default="")
    Gst_enable = models.BooleanField(default=True)
    default_gst = models.IntegerField(default=0)

class Formet(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Inv_prefix = models.CharField(default="INV-")
    Inv_footer = models.CharField(default="Thank you for your purchase! For queries, contact us at shop@billmate.in")
    Inv_due_days = models.IntegerField( default=15)
    Show_signature_area = models.BooleanField(default=True)
    Show_TC = models.BooleanField(default=True)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Customer_name = models.CharField(max_length=255)
    Customer_mobile = models.IntegerField(max_length=10)
    Customer_email = models.EmailField(default="customer@smartbill.com")
    customer_bill_count = models.IntegerField(default=0)
    customer_bill_spent = models.IntegerField(default=0)
    def __str__(self):
        return self.Customer_mobile

class Products(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Product_name = models.CharField()
    Product_price = models.IntegerField()
    Product_stock = models.IntegerField()
    Product_gst = models.IntegerField()

class Invoice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Inv_number = models.IntegerField()
    Inv_Total = models.IntegerField()
    Inv_gst = models.IntegerField()
    Inv_discount = models.IntegerField()
    Inv_additional_charges = models.IntegerField()
    Inv_internal_notes = models.IntegerField()
    Inv_bill_date = models.DateField()
    Inv_due_bill_date = models.DateField()
    Inv_payment_mode = models.CharField()
    Customer_number = models.IntegerField()
    def __str__(self):
        return self.Inv_number

class Sells(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    Inv_number = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    Product_name = models.CharField()
    Product_qty = models.IntegerField()
