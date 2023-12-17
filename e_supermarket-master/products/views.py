# Standard
import re
import json
import datetime
# Third Party
from decimal import Decimal
from dal import autocomplete
# Django
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.template.loader import render_to_string
# Local
from main.functions import get_auto_id, generate_form_errors, get_current_role
from general.models import Location
from products.models import Product, Category, SubCategory, MetaKeyword, ProductVariant
from products.forms import CategoryForm, SubCategoryForm, ProductForm, ProductVariantForm
from customers.models import Customer


class SubCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self, *args, **kwargs):
        category = self.forwarded.get("category")
        if category:
            items = SubCategory.objects.filter(is_deleted=False,category=category)
            if self.q:
                items = items.filter(Q(name__istartswith=self.q))
            return items
        else:
            return SubCategory.objects.none()


@login_required
def categories(request):
    pk = request.GET.get("pk")
    instance = ''
    if pk:
        try:
            instance = Category.objects.get(pk=pk)
        except:
            pass
    if request.method == 'POST':
        if instance:
            form = CategoryForm(request.POST, request.FILES, instance=instance)
        else:
            form = CategoryForm(request.POST, request.FILES)

        auto_id = get_auto_id(Category)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = auto_id
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully created",
                "message": " successfully created.",
                "redirect": "true",
                "redirect_url": reverse('products:categories')
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')

        else:
            message = generate_form_errors(form, formset=False)
            print(form.errors)
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": str(message)
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        instances = Category.objects.filter(is_deleted=False).order_by('date_added')
        if instance:
            form = CategoryForm(instance=instance)
        else:
            form = CategoryForm()

        context = {
            "title": "Categories",
            "instances" : instances,
            "category" : instance,
            "form": form,
            "categories_active" : True,
            "is_need_popup_box" : True,
        }
        return render(request, 'products/categories.html', context)


@login_required
def delete_category(request, pk):
    instance = get_object_or_404(Category, pk=pk)

    Category.objects.filter(pk=pk).delete()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Category Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:categories')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def sub_categories(request):
    instances = SubCategory.objects.filter(is_deleted=False).order_by('-date_added')
    pk = request.GET.get("pk")
    instance = ''
    if pk:
        try:
            instance = SubCategory.objects.get(pk=pk)
        except:
            pass
    if request.method == 'POST':
        if instance:
            form = SubCategoryForm(request.POST, request.FILES, instance=instance)
        else:
            form = SubCategoryForm(request.POST, request.FILES)

        auto_id = get_auto_id(SubCategory)
        if form.is_valid():

            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = auto_id
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully created",
                "message": " successfully created.",
                "redirect": "true",
                "redirect_url": reverse('products:sub_categories')
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
        if instance:
            form = SubCategoryForm(instance=instance)
        else:
            form = SubCategoryForm()

        context = {
            "title": "Sub Categories",
            'instances' : instances,
            "sub_category" : instance,
            "form": form,
            "sub_categories_active" : True,
            "is_need_popup_box" : True,
        }
        return render(request, 'products/sub_categories.html', context)


@login_required
def delete_subcategory(request, pk):
    instance = get_object_or_404(SubCategory, pk=pk)

    SubCategory.objects.filter(pk=pk).delete()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "SubCategory Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:sub_categories')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        variant_form = ProductVariantForm(request.POST, request.FILES)
        auto_id = get_auto_id(Product)
        current_role = get_current_role(request)

        if form.is_valid() and variant_form.is_valid():

            description = request.POST.get('description')
            
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = auto_id
            data.is_verified = True
            
            try:
                meta_keyword_description = data.meta_keyword_description
                split_string = re.split("\s|(?<!\d)[,.](?!\d)", meta_keyword_description)

                # Remove empty strings from list
                while("" in split_string) : 
                    split_string.remove("") 

                #loop meta decription and add to a new model MetaKeyword
                for item in split_string:
                    meta,created = MetaKeyword.objects.get_or_create(
                        name = item
                    )

                    #save metakeyword field as many to many
                    data.meta_keyword.add(meta)
                    data.save()

            except:
                pass

            data.save()
            variant = variant_form.save(commit=False)
            variant.product = data
            variant.save()

            response_data = {
                "status": "true",
                "title": "Successfully created",
                "message": " product created successfully.",
                "redirect": "true",
                "redirect_url": reverse('products:product', kwargs={"pk": data.pk})
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
        form = ProductForm()
        categories = Category.objects.filter(is_deleted=False)
        form.fields["category"].queryset = categories
        variant_form = ProductVariantForm()

        context = {
            "title": "Create Product",
            "url": reverse('products:create_product'),
            "form": form,
            "redirect": True,
            "entry_product_active" : True,
            "is_need_popup_box" : True,
        }
        return render(request, 'products/entry_product.html', context)


@login_required
def edit_product(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    if ProductVariant.objects.filter(is_default=True, is_deleted=False, product=instance).exists():
        variant = ProductVariant.objects.filter(is_default=True,is_deleted=False, product=instance)[0]
    elif ProductVariant.objects.filter(is_deleted=False, product=instance).exists():
        variant = ProductVariant.objects.filter(is_deleted=False, product=instance)[0]
    else:
        variant = ''

    if request.method == 'POST':

        response_data = {}
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if variant:
            variant_form = ProductVariantForm(request.POST, request.FILES, instance=variant)
        else:
            variant_form = ProductVariantForm(request.POST, request.FILES)

        if form.is_valid() and variant_form.is_valid():
            description = request.POST.get('description')

            data = form.save(commit=False)
            data.description = description
            variant_data = variant_form.save(commit=False)
            data.updater = request.user

            try:
                meta_keyword_description = request.POST.get('meta_keyword_description')
                data.mete_keyword_description = meta_keyword_description
                split_string = re.split("\s|(?<!\d)[,.](?!\d)", meta_keyword_description)

                # Remove empty strings from list
                while("" in split_string) : 
                    split_string.remove("") 

                #loop meta decription and add to a new model MetaKeyword
                for item in split_string:
                    meta,created = MetaKeyword.objects.get_or_create(
                        name = item
                    )

                    #save metakeyword field as many to many
                    data.meta_keyword.add(meta)
                    data.save()

            except:
                pass

            data.save()
            variant_data.product = data
            variant_data.save()

            response_data = {
                "status": "true",
                "title": "Successfully updated",
                "message": " successfully updated.",
                "redirect": "true",
                "redirect_url": reverse('products:product', kwargs={"pk": data.pk})
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

        form = ProductForm(instance=instance)
        if variant:
            variant_form = ProductVariantForm(instance=variant)
        else:
            variant_form = ProductVariantForm()

        context = {
            "form": form,
            "variant_form" : variant_form,
            "title": "Edit Product : " + instance.name,
            "instance": instance,
            "entry_product_active" : True,
            "is_need_popup_box" : True,
        }
        return render(request, 'products/entry_product.html', context)


@login_required
def delete_product(request, pk):
    instance = get_object_or_404(Product, pk=pk)

    Product.objects.filter(pk=pk).update(name=instance.name + "_deleted_" + str(instance.id), is_deleted=True)

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Product Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:products')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def product(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    variants = ProductVariant.objects.filter(product=instance)
    title = "Product"

    context = {
        "instance": instance,
        "variants": variants,
        'title': title,
        "product_active" : True,
        "is_need_popup_box" : True,
    }
    return render(request, 'products/product-detail.html', context)


@login_required
def products(request):
    cat_pk = request.GET.get('cat_pk')
    category = ''
    if cat_pk:
        try:
            category = Category.objects.get(pk=cat_pk)
        except:
            pass
    if category:
        instances = Product.objects.filter(is_deleted=False, category=category).order_by('date_added')
    else:
        instances = Product.objects.filter(is_deleted=False).order_by('date_added')

    categories = Category.objects.filter(is_deleted=False).order_by('date_added')

    context = {
        "instances": instances,
        "categories" : categories,
        "active_category" : category,
        "products_active" : True,
        "is_need_popup_box" : True,
    }
    return render(request, 'products/product-list.html', context)


@login_required
def create_product_variant(request,pk):

    instance = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductVariantForm(request.POST, request.FILES)

        if form.is_valid():

            data = form.save(commit=False)
            data.product = instance
            data.save()
            
            if data.is_default:
                ProductVariant.objects.filter(product=instance).exclude(pk=data.pk).update(is_default=False)

            response_data = {
                "status": "true",
                "title": "Successfully created",
                "message": " Product variant created successfully.",
                "redirect": "true",
                "redirect_url": reverse('products:product', kwargs={"pk": instance.pk})
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

        form = ProductVariantForm()

        context = {
            "title": "Create Product Variant",
            "form": form,
            "is_need_popup_box" : True,
        }
        return render(request, 'products/entry_product_variant.html', context)


@login_required
def edit_product_variant(request, pk):

    instance = get_object_or_404(ProductVariant, pk=pk)
    product = instance.product

    if request.method == 'POST':

        response_data = {}
        form = ProductVariantForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            product = instance.product
            product.is_variants = True
            product.save()

            if data.is_default:
                ProductVariant.objects.filter(product=instance).exclude(pk=data.pk).update(is_default=False)

            response_data = {
                "status": "true",
                "title": "Successfully updated",
                "message": " successfully updated.",
                "redirect": "true",
                "redirect_url": reverse('products:product', kwargs={"pk": product.pk})
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

        form = ProductVariantForm(instance=instance)

        context = {
            "form": form,
            "title": "Edit Product Variant",
            "instance": instance,
            "is_need_popup_box" : True,
        }
        return render(request, 'products/entry_product_variant.html', context)


@login_required
def delete_product_variant(request, pk):
    instance = get_object_or_404(ProductVariant, pk=pk)
    product = instance.product
    if instance.is_default:
        if ProductVariant.objects.filter(product=product).exclude(pk=instance.pk).exists():
            variant = ProductVariant.objects.filter(product=product).exclude(pk=instance.pk)[0]
            variant.is_default = True
            variant.save()
        else:
            product.is_variants = False
            product.save()

    instance.delete()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Variant Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('products:product', kwargs={"pk": product.pk})
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def product_variant(request, pk):
    instance = get_object_or_404(ProductVariant, pk=pk)
    title = "Product Variant"

    context = {
        "instance": instance,
        'title': title,
    }
    return render(request, 'products/product_variant.html', context)
