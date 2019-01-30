from django.contrib import admin
from .models import ProductModel, CartModel, ShippingModel, OrderModel

class ProductAdmin(admin.ModelAdmin):
    list_display =['id', 'name', 'price']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','cartID', 'price', 'quantity', 'product']

class ShippingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'date', 'paid']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'quantity', 'date_added', 'shipping']


admin.site.register(ProductModel, ProductAdmin)
admin.site.register(CartModel, CartAdmin)
admin.site.register(ShippingModel, ShippingAdmin)
admin.site.register(OrderModel, OrderAdmin)
