# Django
from django import forms
from django.forms.widgets import TextInput,Textarea,Select,DateInput, CheckboxInput
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Local
from customers.models import CustomerAddress


class CustomerAddressForm(forms.ModelForm):

    class Meta:
        model = CustomerAddress
        fields = ['address','landmark','save_as','house_flat_block_no']

        widgets = {
            'address': Textarea(attrs={'class': 'form-control','placeholder' : 'Address'}),
            'landmark' : TextInput(attrs={'class': 'required form-control','placeholder' : 'Landmark'}),
            'save_as': Select(attrs={'class': 'form-control selectpicker','placeholder' : 'Save This Address As '}),
            'house_flat_block_no': TextInput(attrs={'class': 'form-control', 'placeholder' : 'House/Flat/Block Number'}),
        }