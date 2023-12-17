from dal import autocomplete
# Django
from django import forms
from django.forms.widgets import TextInput,Textarea,Select,DateInput, CheckboxInput
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Local
from products.models import Product, Category, SubCategory, ProductVariant


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ['creator','updater','auto_id','is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Category Name'}),
        }


class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory
        exclude = ['creator','updater','auto_id','is_deleted']
        widgets = {
            'name': TextInput(attrs={'class': 'required form-control','placeholder' : 'Name'}),
            'category': Select(attrs={'class': 'required form-control selectpicker','placeholder' : 'Product Category','required':'required'}),

        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['creator','updater','auto_id','is_deleted','meta_keyword','is_variants','sub_category']
        widgets = {
            'name' : TextInput(attrs={'class': 'required form-control','placeholder' : 'Name'}),
            'category' : Select(attrs={'class': 'required form-control selectpicker','placeholder' : 'Category','required':'required'}),
            'status' : Select(attrs={'class': 'required form-control selectpicker','placeholder' : 'Status','required':'required'}),
            # 'sub_category' : autocomplete.ModelSelect2(url='products:sub_category_autocomplete', forward= ["category"], 
            #     attrs={'class': 'form-control','data-placeholder': 'Sub Category','data-minimum-input-length': 0,'data-autocomplete-light-forward':'category'}),
            'gst' : TextInput(attrs={'class': 'form-control','placeholder' : 'Name'}),
            'description' : Textarea(attrs={'class': 'form-control','placeholder' : 'Description'}),
            'meta_keyword_description': Textarea(attrs={'class': 'form-control','placeholder' : 'Meta Keywords'}),
        }


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        exclude = ['is_deleted','is_verified','product','id','product','out_of_stock_date']
        widgets = {
            'title' : TextInput(attrs={'class': 'required form-control','placeholder' : 'eg:250gram,half,M blue'}),
            'mrp': TextInput(attrs={'class': 'required form-control','placeholder' : 'Mrp'}),
            'price': TextInput(attrs={'class': 'required form-control','placeholder' : 'Price'}),
            'stock' : TextInput(attrs={'class': 'required form-control','placeholder' : 'Stock'}),
        }
