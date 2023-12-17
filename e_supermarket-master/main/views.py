#Standard
import logging
import datetime
#Third Party
from decimal import Decimal
from datetime import datetime, timedelta
#Django
from django.shortcuts import render
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
#Local Libraries
from main.functions import get_current_role
from products.models import Product, ProductVariant, Category
from customers.models import Customer
from orders.models import Order


# @check_mode
@login_required
def app(request):
    current_role = get_current_role(request)
    print("current_role",current_role)
    if current_role == 'superadmin':
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return HttpResponseRedirect(reverse('web:index'))


# @check_mode
@login_required
def dashboard(request):
    today = datetime.now().date()

    today_date = datetime.now()
    days_7_left = timedelta(7)
    new_date = today_date - days_7_left
    weekly_date = new_date.date()

    total_revenue = Order.objects.filter(status="delivered",is_deleted=False).aggregate(total=Sum('amount_payable')).get("total",0)
    total_products = Product.objects.filter(is_deleted=False).count()
    total_categories = Category.objects.filter(is_deleted=False).count()
    total_orders = Order.objects.filter(is_deleted=False).count()
    new_orders = Order.objects.filter(is_deleted=False,date_added__date=today).count()
    total_customers = Customer.objects.filter(is_active=True, is_deleted=False).count()
    new_customers = Customer.objects.filter(is_active=True, is_deleted=False, date_added__date__gte=weekly_date).count()

    if not total_revenue:
        total_revenue = 0

    context = {
        "dashboard_active" : True,
        "total_products" : total_products,
        "total_categories" : total_categories,
        "total_orders" : total_orders,
        "new_orders" : new_orders,
        "total_customers" : total_customers,
        "new_customers" : new_customers,
        "total_revenue" : total_revenue,
    }
    return render(request, "index.html",context)

