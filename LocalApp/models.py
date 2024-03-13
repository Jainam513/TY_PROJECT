from collections import UserDict
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    # image = models.FileField(null=True, blank=True)
   
    
    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(max_length=1000, null=True)
    stime = models.TextField(max_length=500,null=True)
    image = models.FileField(null=True, blank=True)
   # discount = models.CharField(max_length=100, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.name


class Worker(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,null=True)
    image = models.FileField(null=True)
    imgs = models.FileField(null=True)
    professional = models.CharField(max_length=35,null=True)
    email = models.EmailField(null=True)
    address = models.TextField(max_length=800,null=True)
    type = models.CharField(max_length=15,null=True)
    status = models.CharField(max_length=15,null=True)
    auth_token = models.CharField(max_length=100,null=True) 
    # null=true video ma nathi pan me karyu
    is_verified = models.BooleanField(default=False,null=True)
    

    def __str__(self):
        return self.user.username
    
    
class Contact(models.Model):
    name = models.CharField(max_length=60)
    email=models.EmailField()
    subject = models.CharField(max_length=1000)
    
    
    def __str__(self):
        return self.name
    
    #for custm
    
# customer login class

class Customer(models.Model):
    user = models.ForeignKey (User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
   
    def __str__(self):
        return self.user.username
    
    
    
    
#card
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.TextField(default={'objects': []}, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    
    
    
    
    
    
#booking table
ORDERSTATUS = ((1, "Pending"),  (2, "On the way"), (3, "Delivered"), (4, "Done"))
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.TextField(default={'objects': []}, null=True, blank=True)
    total = models.CharField(max_length=100, null=True, blank=True)
    # stime = models.TextField(max_length=500,null=True)
    status = models.IntegerField(choices=ORDERSTATUS, default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    
    # def save(self,*args, **kwargs):
    #     if self.order_id is None and self.detetime_of_payment and self.id:
    #         self.order_id = self.detetime_of_payment('PAY2%Y%m%dODR')+str(self.id)
    #     return super.save(*args,**kwargs)
    
    
    
    
STATUS = ((1, "Read"), (2, "Unread"))
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
STATUS = ((1, "Read"), (2, "Unread"))
class Worker_Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    
    
class WPay(models.Model):
    email = models.EmailField(null=True)
    name = models.CharField(max_length=100)
    amount=models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paide =models.BooleanField(default=False)
    
    def __str__(self):
        return self.name