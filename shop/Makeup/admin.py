from django.contrib import admin
from .models import Products,Order,OrderItem,Cart,CartItem
# Register your models here.

admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
