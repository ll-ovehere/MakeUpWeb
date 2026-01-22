from django.db import models
from django.core.validators import MaxLengthValidator,MinLengthValidator
# Create your models here.

class Products(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,verbose_name='name')
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='price')
    image=models.FileField(upload_to='images',null=True)
    def __str__(self):
        return self.name 
      
class Custmor(models.Model):
    id=models.AutoField(primary_key=True)
    email=models.EmailField(unique=True,max_length=12)
    password=models.TextField(max_length=10)

class Order(models.Model):
    id=models.AutoField(primary_key=True)
    custmor=models.ForeignKey(
        Custmor,
        on_delete=models.CASCADE
    )
    total_price=models.BigIntegerField(max_length=4,verbose_name='total_price')
    def __str__(self):
        return f"Order #{self.id}"
      
class OrderItem(models.Model):
    id=models.AutoField(primary_key=True)
    order=models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    product=models.ForeignKey(
        Products,
        on_delete=models.CASCADE
    )
    quantity=models.PositiveBigIntegerField(default=1)
    def __str__(self):
        return f"{self.quantity}{self.product}" 
    
class Cart(models.Model):
    id=models.AutoField(primary_key=True)
    custmor=models.ForeignKey(
        Custmor,
        on_delete=models.CASCADE
    )   

class CartItem(models.Model):
    id=models.AutoField(primary_key=True)
    cart=models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )
    product=models.ForeignKey(
        Products,
        on_delete=models.CASCADE
    )
    quantity=models.PositiveBigIntegerField(default=1)
   
