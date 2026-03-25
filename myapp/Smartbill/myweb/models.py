from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.ImageField(max_length=10)
    def __str__(self):
        return self.email

class Business(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bizType = models.CharField()
    Gstin = models.CharField()
    City = models.CharField()
    full_address = models.TextField()
    Pan_number =models.CharField()
    shop_logo = models.ImageField()
    Gst_enable = models.BinaryField(default=True)
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
    Customer_email = models.EmailField()
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
