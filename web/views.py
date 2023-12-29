import json
import datetime
#Django
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q, F
from django.db.models import Sum, Avg
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
# Local
from main.functions import get_auto_id, generate_form_errors, get_current_role, randomnumber
from general.functions import get_or_create_location, get_location_distance, send_sms
from customers.models import Customer, Cart, CartItem, CustomerAddress
from customers.forms import CustomerAddressForm
from products.models import Category, SubCategory, Product, ProductVariant
from products.functions import update_stock
from general.models import Location, BannerImages, ShopDetails
from orders.models import Order, OrderItem


def index(request):
    banner_images = BannerImages.objects.filter(is_deleted=False, status="active")
    context = {
        "banner_images" : banner_images,
    }
    return render(request, 'web/index.html',context)
        

def about(request):
    return render(request, 'web/about.html')


def contact(request):
    return render(request, 'web/contact.html')


def store(request):
    instances = ''
    if request.method == "POST":
        search_content = request.POST.get("search")
        print("search", search_content)
        instances = Product.objects.filter(status="active", is_deleted=False).filter(Q(name__icontains=search_content) | Q(category__name__icontains=search_content) | Q(
            sub_category__name__icontains=search_content) | Q(meta_keyword__name__icontains=search_content))
    print("instances",instances)
    context = {
        "instances" : instances,
    }

    return render(request, 'web/store.html', context)
        

def cart(request):
    instance = Cart.objects.get(customer__user=request.user)
    items = CartItem.objects.filter(cart=instance, is_deleted=False)

    context = {
        "instance" : instance,
        "items" : items
    }
    return render(request, 'web/cart.html', context)


def customer_login(request):
    otp_send_url = reverse("web:otp_send")
    verify_otp_url = reverse("web:verify_otp")

    context = {
        "otp_send_url" : otp_send_url,
        "verify_otp_url" : verify_otp_url, 
    }

    return render(request, 'web/login.html',context)


def items(request,pk):
    page_num = request.GET.get("page_no")
    
    category = get_object_or_404(Category, pk=pk)

    total_products = Product.objects.filter(status="active", is_deleted=False, category=category).count()
    total_pages = total_products // 12
    pages = total_products % 12
    if pages > 0:
        total_pages += 1

    if not page_num:
        page_num = 1
    page_num = int(page_num)
    index = page_num * 12
    start = index - 12

    pagination = False
    if total_pages > 1:
        pagination = True

    items = Product.objects.filter(is_deleted=False, category=category)[start:index]

    context = {
        "items" : items,
        "category" : category,
        "pagination" : pagination,
        "page_num" : page_num,
        "total_pages" : total_pages * "a",
    }
    return render(request, 'web/items.html', context)
        

def item_details(request, pk):
    variant_pk = request.GET.get("variant")
    item = get_object_or_404(Product, pk=pk)
    if variant_pk:
        default_variant = ProductVariant.objects.get(is_deleted=False, product=item, pk=variant_pk)
    else:
        default_variant = item.default_variant
        
    variants = ProductVariant.objects.filter(is_deleted=False, product=item)

    context = {
        "item" : item,
        "default_variant" : default_variant,
        "variants" : variants
    }
    return render(request, 'web/item-detail-2.html', context)


def register(request):
    otp_send_url = reverse("web:otp_send")
    verify_otp_url = reverse("web:verify_otp")
    context = {
        "otp_send_url" : otp_send_url,
        "verify_otp_url" : verify_otp_url, 
    }
    return render(request, 'web/register.html', context)
    

def otp_send(request):  
    phone = request.GET.get('phone')
    action = request.GET.get('action')
    if action == "register":
        name =  request.GET.get('name')
        if Customer.objects.filter(phone=phone, is_active=True).exists():
            response_data = {
                "status": "false",
                "title": "Phone Number Exist",
                "message": "You entered mobile number already exist, please log in"
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            if Customer.objects.filter(phone=phone, is_active=False).exists():
                customers = Customer.objects.filter(phone=phone, is_active=False)
                for customer in customers:
                    if customer.user.is_active == False:
                        customer.user.delete()
                Customer.objects.filter(phone=phone, is_active=False).delete()

            #create customer
            data = Customer.objects.create(phone=phone, name=name) 

            user = User.objects.create_user(
                    username=phone,
                    password=phone,
                    is_staff=False,
                    is_active=False,
                )

            group = Group.objects.get(name="customer")
            user.groups.add(group)
            user.save()

            otp = randomnumber(4)
            print("---otp---: ",otp)

            data.otp = otp
            data.user = user
            data.save()

            # Send SMS
            if not phone == "1111111111":
                # send_sms(phone, otp)
                pass

            response_data = {
                "status": "true",
                "title": "OTP sent.",
                "message": "Continue, and Verify Otp.",
            }
    else:
        if not Customer.objects.filter(phone=phone, is_active=True).exists():
            response_data = {
                "status": "false",
                "title": "Invalid Phone Number",
                "message": "Invalid Phone Number."
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')
        else:
            data = Customer.objects.get(phone=phone)
            otp = randomnumber(4)
            print("---otp---: ",otp)

            data.otp = otp
            data.save()

            # Send SMS
            sms_message1 = "Dear customer, %s is your OTP for registering in E Market application. Don't share your OTP with anyone." % (otp)
            sms_message = str(sms_message1) 

            if not phone == "1111111111":
                # sendSMS(phone, sms_message)
                pass

            response_data = {
                "status": "true",
                "title": "OTP sent.",
                "message": "Continue, and Verify Otp.",
            }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


def verify_otp(request):
    phone = request.GET.get('phone')
    otp = request.GET.get('otp')
    action =  request.GET.get('action')
    redirect_url = request.GET.get("redirect_url")
    print(phone,"\t",otp,"\t",action,"\t",redirect_url)
    if Customer.objects.filter(phone=phone).exists():
        customer = Customer.objects.get(phone=phone)
        if customer.otp == otp:
            user = customer.user
            if action == "register":
                Customer.objects.filter(phone=phone, otp=otp).update(is_active=True)
                user.is_active = True
                user.save()
            else:
                pass

            login(request, user)
            response_data = {
                "status": "true",
                "title": "success.",
                "message": "Login Successfully",
                "redirect_url" : reverse("web:index")
            }

        else:
            response_data = {
                "status": "false",
                "title": "Invalid Otp.",
                "message": "Invalid Otp",
            }

    else:
        response_data = {
            "status": "true",
            "title": "Invalid Mobile Number.",
            "message": "Invalid Mobile Number",
        }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def customer_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('web:index'))


@login_required
def add_to_cart(request,pk):
    qty = request.GET.get('qty')

    if not qty:
        qty = 1

    try:
        product_variant = ProductVariant.objects.get(pk=pk)
        product = product_variant.product
    except:
        response_data = {
            "status" : "false",
            "message" : "Product does not exists",
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    try:
        customer = Customer.objects.get(user=request.user)
    except:
        response_data = {
            "status" : "false",
            "message" : "Please log in",
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    try:
        cart = Cart.objects.get(customer = customer)
    except:
        cart = Cart.objects.create(
            customer = customer,
            auto_id = get_auto_id(Cart),
            creator = request.user,
            updater = request.user,
            total = 0
        )

    if CartItem.objects.filter(cart=cart,product_variant=product_variant,is_deleted=False).exists():
        cart_item_count = CartItem.objects.filter(cart=cart, is_deleted=False).count()
        response_data = {
            "status" : "false",
            "message" : "Item exists in Cart",
            "cart_item_count" : str(cart_item_count),
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        CartItem.objects.create(
            product_variant = product_variant,
            cart = cart,
            qty = qty,
            price = product_variant.price,
            subtotal = product_variant.price * (int(qty))
        )
        cart.total += product_variant.price * (int(qty))
        cart.save()
        cart_item_count = CartItem.objects.filter(cart=cart, is_deleted=False).count()
        
        response_data = {
            "status" : "true",
            "message" : "Added to Cart",
            "cart_item_count" : str(cart_item_count),
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def clear_cart(request):
    try:
        customer = Customer.objects.get(user=request.user)
        if Cart.objects.filter(customer=customer).exists():
            cart = Cart.objects.get(customer=customer)
            cart_items = CartItem.objects.filter(cart=cart, is_deleted=False)
            if cart_items:
                CartItem.objects.filter(cart=cart, is_deleted=False).delete()
            cart.total = 0
            cart.save()
    except:
        pass
    
    return HttpResponseRedirect(reverse('web:index'))


@login_required
def cart_quantity_update(request, pk):
    action = request.GET.get('action')
    instance = get_object_or_404(CartItem, pk=pk)
    cart = instance.cart
    if action == "plus" :
        stock = instance.product_variant.stock
        if stock > instance.qty:
            instance.qty += 1
            instance.subtotal += instance.price
            cart.total += instance.price
            instance.save()
            cart.save()
    elif action == "minus" :
        instance.qty -= 1
        instance.subtotal -= instance.price
        cart.total -= instance.price
        instance.save()
        cart.save()

    qty = instance.qty
    if qty <= 0 :
        instance.delete()

    if CartItem.objects.filter(is_deleted=False, cart=cart).exists():
        return HttpResponseRedirect(reverse('web:cart'))
    else:
        return HttpResponseRedirect(reverse('web:index'))


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    sub_total = cart_item.subtotal
    cart = cart_item.cart
    cart_item.delete()

    cart.total -= sub_total
    cart.save()

    if CartItem.objects.filter(is_deleted=False, cart=cart).exists():
        return HttpResponseRedirect(reverse('web:cart'))
    else:
        return HttpResponseRedirect(reverse('web:index'))


@login_required
def checkout(request):
    address_pk = request.GET.get("address")
    customer = Customer.objects.get(user=request.user)
    shop = ShopDetails.objects.first()
    if request.method == "POST":
        form = CustomerAddressForm(request.POST, request.FILES)
        if form.is_valid():
            
            data = form.save(commit=False)
            data.is_active = True
            data.customer = customer
            data.phone = customer.phone
            data.name = customer.name

            location_name = request.POST.get('location_name')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            destination = (latitude,longitude)

            distance_result = get_location_distance(request,destination)
            is_ok = False
            distance = distance_result["distance"]
            distance = distance / 1000
            duration = distance_result["duration"]
            try:
                max_distance = shop.distance_covered
                if distance:
                    if distance <= float(max_distance):
                        is_ok = True
            except:
                pass

            if is_ok:
                location = get_or_create_location(request,location_name,latitude, longitude)
                data.location = location
                try:
                    data.total_distance = (distance /1000)
                    data.total_duration = duration
                except:
                    pass

                data.save()
                CustomerAddress.objects.exclude(pk=data.pk).update(is_active=False)

                response_data = {
                    "status": "true",
                    "title": "Successfully created",
                    "message": "Address added successfully.",
                    "redirect": "true",
                    "redirect_url": reverse('web:checkout')
                }
            else:
                response_data = {
                    "status": "false",
                    "stable": "true",
                    "title": "service not available",
                    "message": "sorry.service not available at your location",
                }

            return HttpResponse(json.dumps(response_data), content_type='application/javascript')

        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": str(message)
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        form = CustomerAddressForm()
        instance = Cart.objects.get(customer__user=request.user)
        items = CartItem.objects.filter(cart=instance, is_deleted=False)
        addresses = CustomerAddress.objects.all()
        active_address = ''
        if addresses:
            if address_pk:
                active_address = addresses.get(pk=address_pk)
                active_address.is_active = True
                active_address.save()
                CustomerAddress.objects.exclude(pk=address_pk).update(is_active=False)
            addresses = CustomerAddress.objects.all()
            if addresses.filter(is_active=True).exists():
                active_address = addresses.filter(is_active=True)[0]
            else:
                active_address = addresses[0]
                active_address.is_active = True
                active_address.save()

        free_delivery_amount = shop.free_delivery
        total_amount = instance.total
        amount_payable = total_amount
        if total_amount >= free_delivery_amount:
            delivery_charge = "Free Shipping"
        else:
            delivery_charge = shop.delivery_charge
            amount_payable += shop.delivery_charge
                
        context = {
            "instance" : instance,
            "form" : form,
            "items" : items,
            "addresses" : addresses,
            "active_address" : active_address,

            "delivery_charge" : delivery_charge,
            "amount_payable" : amount_payable,

            "location_name" : shop.location.location_name,
            "latitude" : shop.location.latitude,
            "longitude" : shop.location.longitude,

            "is_need_popup_box" : True,
        }
        return render(request, 'web/checkout.html', context)


@login_required
def place_order(request):

    # payment_method = request.GET.get('payment_method')
    payment_method = "cash on delivery"

    try:
        shop = ShopDetails.objects.first()
    except:
        shop = ''

    try:
        customer = Customer.objects.get(user=request.user) 
    except:
        response_data = {
            "status": "false",
            "title": "Permission Denied.",
            "message": "You cannot Shoping here.",
            "redirect": "true",
            "redirect_url": reverse('web:login')
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    item_exists = False
    try:
        cart = Cart.objects.get(customer=customer)
        cart_items = CartItem.objects.filter(cart=cart, is_deleted=False)
        if cart_items:
            item_exists = True
    except:
        pass

    if not item_exists:
        response_data = {
            "status": "false",
            "title": "Your Cart is Empty",
            "message": "Add Items To Cart",
            "redirect": "true",
            "redirect_url": reverse('web:index_page')
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    if CustomerAddress.objects.filter(customer=customer, is_active=True).exists():
        customer_address = CustomerAddress.objects.filter(customer=customer, is_active=True)[0]
    else: 
        customer_address = ''     
    
    if not customer_address:
        response_data = {
            "status": "false",
            "title": "Add Your Address.",
            "address_message": "Please add your address",
            "stable" : "true"
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    elif not payment_method:
        response_data = {
            "status": "false",
            "title": "Choose Payment Method.",
            "payment_message": "Please select payment method",
            "stable" : "true"
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        total_amount = cart.total
        subtotal_amount = total_amount

        delivery_charge = 0

        amount_payable = total_amount
        if shop:
            free_delivery_amount = shop.free_delivery
            if total_amount >= free_delivery_amount:
                delivery_charge = 0
            else:
                delivery_charge = shop.delivery_charge
                amount_payable += shop.delivery_charge

        today = datetime.date.today()
        order_auto_id = get_auto_id(Order)
        order_id = "OR" + str(today.day).zfill(2) + str(today.month).zfill(2) + str(order_auto_id).zfill(3)
        data = Order.objects.create(
            customer = customer,
            creator = request.user,
            updater = request.user,
            order_id = order_id,
            auto_id = order_auto_id,
            billing_address = customer_address,
            amount_payable = amount_payable,
            total_amount = total_amount,
            delivery_charge = delivery_charge,
            payment_method = payment_method,
            total_distance = 1,
            time_duration = 1,
            sub_total = subtotal_amount,
        )

        total_discount_amount = 0
        total_subtotal = 0
        for item in cart_items :
            # create a dealer vise orderitem
            product_variant = item.product_variant
            price = item.price
            mrp = item.product_variant.mrp
            qty = item.qty
        
            # total discount price of this x product
            discount_amount = (mrp - price) * qty

            total_discount_amount += discount_amount

            # total subtotal of this x product
            subtotal = (item.qty * price)
            total_subtotal += subtotal

            value = OrderItem.objects.create(
                order = data,
                product_variant = product_variant,
                qty = qty,
                price = price,
                discount_amount = discount_amount,
                subtotal = subtotal,
            )

            update_stock(request, item.product_variant.pk, item.qty, "decrease")
            product_instance = item.product_variant.product
            item.delete()

        # update total tax and discount amounts
        data.total_amount = total_subtotal
        # data.amount_payable = float(total_subtotal) + delivery_charge
        data.discount_amount = total_discount_amount

        cart.total = 0
        cart.save()

        # create_notification(request, "new_order", data)

        response_data = {
            "status": "true",
            "title": "Order Success.",
            "message": "Your order success.",
            "redirect": "true",
            "redirect_url": reverse('web:orders')
        }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def orders(request):

    customer = get_object_or_404(Customer,user=request.user)
    orders = Order.objects.filter(customer=customer, is_deleted=False)
    total_orders = orders.count()

    addresses = CustomerAddress.objects.all()

    context = {
        "title" : "My Orders",
        "customer" : customer,
        "orders" : orders,
        "addresses" : addresses,
    }
    
    return render(request, 'web/your-orders.html', context)


@login_required
def order_details(request,pk):

    instance = get_object_or_404(Order,pk=pk)
    items = instance.order_items

    context = {
        "title" : "My Orders",
        "instance" : instance,
        "items" : items,
    }
    
    return render(request, 'web/order-details.html', context)




