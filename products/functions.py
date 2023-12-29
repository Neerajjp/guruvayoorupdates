import datetime
from products.models import ProductVariant


def update_stock(request,pk,qty,status):
    product = ProductVariant.objects.get(pk=pk)
    stock = product.stock
    if status == "increase":
        balance_stock = stock + qty
    elif status == "decrease":
        balance_stock = stock - qty

    product.stock=balance_stock
    if balance_stock <= 0:
        today = datetime.datetime.now()
        product.out_of_stock_date = today
        # create_notification(request, "low_stock_notification", product)
    product.save()