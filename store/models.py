from django.db import models
from django.contrib.auth.models import User
import datetime
import os
# from django.db.models.deletion import SET_NULL
# from django.db.models.fields import CharField, reverse_related
# Create your models here.
class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product', on_delete=models.SET_NULL , null=True ,blank=True, related_name='+')
    def __str__(self):
        return self.title


class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()

    def __str__(self):
        return self.description

def filepath(request,filename):
    old_name=filename
    current_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename="%s%s" % (current_time,old_name)
    return os.path.join("uploads/",filename)

class Product(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    unit_price=models.DecimalField(max_digits=8 , decimal_places=2 )
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions=models.ManyToManyField(Promotion , blank=True)
    img = models.ImageField(upload_to=filepath, blank=True)

    def __str__(self):
        return self.title


class Customer(models.Model):
    member_bronze="B"
    member_silver="S"
    member_gold="G"
    membership_choices=[
        (member_bronze,"Bronze"),
        (member_silver,"Silver"),
        (member_gold,"Gold")

    ]
    # first_name=models.CharField(max_length=255)
    # last_name=models.CharField(max_length=255)
    # email=models.EmailField(unique=True)
    phone=models.CharField(max_length=255)
    Birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1, choices=membership_choices , default=member_bronze)
    user=models.OneToOneField(User,on_delete=models.CASCADE ,null=True,blank=True)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    def __str__(self):
        return self.street
    

class Order(models.Model):
    payment_pending="P"
    payment_complete="C"
    payment_failed="F"
    payment_status_choices=[
        (payment_pending,"Pending"),
        (payment_complete,"Complete"),
        (payment_failed,"Failed")

    ]
    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=1, choices=payment_status_choices , default=payment_pending)
    customer=models.ForeignKey(Customer, on_delete=models.PROTECT)
    def __str__(self):
        return f'{self.customer.user.first_name} {self.customer.user.last_name}'

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.PROTECT)
    product=models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=8 , decimal_places=2 ) 
    def __str__(self):
        return self.product.title

    def get_total_price(self):
        return self.quantity*self.product.unit_price

class Cart(models.Model):
    # customer=models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True, null=True)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.created_at
    


class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField()
   
    # def __str__(self):
    #     return self.product
    def get_total_price(self):
        return self.quantity*self.product.unit_price