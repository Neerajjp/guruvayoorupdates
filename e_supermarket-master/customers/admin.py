from django.contrib import admin
from customers.models import Customer, Cart, CartItem


admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)