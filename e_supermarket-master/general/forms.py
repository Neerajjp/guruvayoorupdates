# Django
from django import forms
from django.forms.widgets import TextInput,Textarea,Select,DateInput, CheckboxInput
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Local
from general.models import ShopDetails, Location, BannerImages


class ShopForm(forms.ModelForm):
    class Meta:
        model = ShopDetails
        exclude = ['creator','updater','auto_id','is_deleted','user','location','is_closed']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["location_name","latitude","longitude"]


class BannerImagesForm(forms.ModelForm):
    class Meta:
        model = BannerImages
        exclude = ['creator','updater','auto_id','is_deleted']
