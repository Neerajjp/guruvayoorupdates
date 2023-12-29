from main.functions import get_current_role
from customers.models import Customer, CartItem
from products.models import Category, SubCategory


def web_context(request):
    cart_items_count = 0
    wishlist_items_count = 0
    is_customer = False
    cart_items_pk = []

    categories = Category.objects.filter(is_deleted=False).order_by("date_added")
    
    current_role = get_current_role(request)
    if current_role == "customer":
        is_customer = True
        cart_items_pk = CartItem.objects.filter(cart__customer__user=request.user, is_deleted=False).values_list("product_variant__pk",flat=True)
        cart_items_count = CartItem.objects.filter(cart__customer__user=request.user, is_deleted=False).count()
    else:
        pass

    path = request.META["PATH_INFO"]
    
    return {
        "path" : path,
        "is_customer" : is_customer,
        "cart_items_count" : cart_items_count,
        "wishlist_items_count" : wishlist_items_count,
        "cart_items_pk" : cart_items_pk,

        "categories" : categories,
    }