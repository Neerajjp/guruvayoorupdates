#Standard
import string
import random
#Third Party
from random import randint
#Django
from django.template import Context
from django.http import HttpResponse
from django.contrib.auth.models import User
#Local


def generate_unique_id(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_form_errors(args,formset=False):
    i = 1
    message = ""
    if not formset:
        for field in args:	
            if field.errors:
                message += "\n"
                message += field.label + " : "
                message += str(field.errors)

        for err in args.non_field_errors():
            message += str(err)
    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message += "\n"
                    message += field.label + " : "
                    message += str(field.errors)
            for err in form.non_field_errors():
                message += str(err)

    message = message.replace("<li>", "")
    message = message.replace("</li>", "")
    message = message.replace('<ul class="errorlist">', "")
    message = message.replace("</ul>", "")
    return message
    

def get_auto_id(model):
    auto_id = 1
    try:
        latest_auto_id =  model.objects.all().order_by("-date_added")[:1]
        if latest_auto_id:
            for auto in latest_auto_id:
                auto_id = auto.auto_id + 1
    except:
        pass
    return auto_id


def get_current_role(request):
    is_superadmin = False
    is_staff = False
    is_customer = False

    if request.user.is_authenticated:        
        
        if User.objects.filter(id=request.user.id,is_superuser=True,is_active=True).exists():
            is_superadmin = True
        
        if User.objects.filter(id=request.user.id,is_active=True,groups__name="staff").exists():
            is_staff = True

        if User.objects.filter(id=request.user.id,is_active=True,groups__name="customer").exists():
            is_customer = True            

    current_role = "user"
    
    if is_superadmin:
        current_role = "superadmin"
    elif is_staff:
        current_role = "staff"
    elif is_customer:
        current_role = "customer"
    return current_role


def randomnumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)