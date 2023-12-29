# Standard
import json
import datetime
from decimal import Decimal
# Django
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Local
from orders.models import Order, OrderItem
from products.models import ProductVariant, Product


@login_required
def orders(request):
    
    today = datetime.datetime.now().date()

    total_orders = 0
    pending_orders = 0
    delivered_orders = 0
    packed_orders = 0
    cancelled_orders = 0

    instances = Order.objects.filter(is_deleted=False)
    # .exclude(date_added__date=today)
    today_orders = Order.objects.filter(is_deleted=False, date_added__date=today)
    try:
        total_orders = Order.objects.filter(is_deleted=False).count()
        pending_orders = Order.objects.filter(is_deleted=False, status="pending").count()
        delivered_orders = Order.objects.filter(is_deleted=False, status="delivered").count()
        packed_orders = Order.objects.filter(is_deleted=False, status="packed").count()
        cancelled_orders = Order.objects.filter(is_deleted=False, status="cancelled").count()
    except:
        pass

    context = {
        "instances" : instances,
        "title" : "Orders",
        "today_orders" : today_orders,

        "total_orders" : total_orders,
        "pending_orders" : pending_orders,
        "delivered_orders" : delivered_orders,
        "packed_orders" : packed_orders,
        "cancelled_orders" : cancelled_orders,
        "orders_active" : True
    }

    return render(request, "orders/order-list.html", context) 


@login_required
def order(request, pk):
    instance = get_object_or_404(Order, pk=pk)
    
    order_items = instance.order_items

    context = {
        "instance" : instance,
        "order_items" : order_items,
    }
    return render(request, "orders/order-detail.html", context) 


@login_required
def update_order_status(request, pk):
    instance = get_object_or_404(Order, pk=pk)
    old_status = instance.status
    status = request.GET.get("status")
    print("status",status)

    instance.status = status
    instance.save()

    if status == "cancelled":
        order_items = OrderItem.objects.filter(order=instance)
        for item in order_items:
            if ProductVariant.objects.filter(pk=item.product_variant.pk, is_deleted=False).exists():
                stock = ProductVariant.objects.get(pk=item.product_variant.pk, is_deleted=False)
                stock.stock += item.qty
                stock.save()

    return redirect(reverse("orders:order", kwargs={"pk":instance.pk}))