import uuid
from decimal import Decimal
from versatileimagefield.fields import VersatileImageField
# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
# Local
from main.models import BaseModel


STATUS_CHOICES = (
    ('active','active'),
    ('disabled','disabled'),
)


class ShopDetails(BaseModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, blank=True, null=True)
    shop_name = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=10, null=True)
    phone2 = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(blank=True,null=True)
    pincode = models.CharField(max_length=10 ,blank=True,null=True)
    location = models.ForeignKey("general.Location",limit_choices_to={'is_deleted': False},on_delete=models.CASCADE,null=True,blank=True)

    shop_image = VersatileImageField('Shop Image',upload_to='shops/featured_images',blank=True, null=True)
    logo = VersatileImageField('Logo',upload_to='shops/featured_images',blank=True, null=True)
    description = models.TextField(blank=True,null=True)

    account_number = models.CharField(max_length=20, blank=True,null=True)
    account_holder_name = models.CharField(max_length=128, blank=True,null=True)
    ifsc_code = models.CharField(max_length=20, blank=True,null=True)
    bank_name = models.CharField(max_length=128, blank=True,null=True)
    branch_name = models.CharField(max_length=128, blank=True,null=True)

    gst_percentage = models.DecimalField(default=0.0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))], blank=True,null=True)
    license = models.CharField(max_length=128, blank=True,null=True)
    license_number = models.CharField(max_length=128, blank=True,null=True)

    distance_covered = models.DecimalField(default=0.0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))], blank=True,null=True)
    delivery_charge = models.DecimalField(default=0.0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))], blank=True,null=True)
    charge_per_km = models.DecimalField(default=0.0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))], blank=True,null=True)
    free_delivery = models.DecimalField(default=0.0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))], blank=True,null=True)

    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    next_opening = models.DateTimeField(null=True, blank=True)

    facebook_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)

    whatsapp_number = models.CharField(max_length=10, null=True,blank=True)

    is_closed = models.BooleanField(default=False)

    def get_logo(self):
        if self.logo:
            try:
                image = self.logo.crop['100x100'].url
            except:
                image = self.logo.url
        else:
            image = ''
        return image

    class Meta:
        db_table = 'shop'
        verbose_name = _('Shop')
        verbose_name_plural = _('Shop Details')
    
    def __str__(self): 
        return self.shop_name


class Location(BaseModel):
    location_name = models.CharField(max_length=128, null=True)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.CharField(max_length=128)
    longitude = models.CharField(max_length=128)

    class Meta:
        db_table = 'general_location'
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return str(self.location_name)


class BannerImages(BaseModel):
    title = models.CharField(max_length=128, null=True)
    image = VersatileImageField('Banner Image',upload_to='shops/banner_images')
    token_id = models.CharField(unique=True, max_length=128)
    status = models.CharField(choices=STATUS_CHOICES, max_length=128)   

    def get_image(self):
        if self.image:
            try:
                image = self.image.crop['600x600'].url
            except:
                image = self.image.url
        else:
            image = ''
        return image

    class Meta:
        db_table = 'banner_images'
        verbose_name = _('Banner Image')
        verbose_name_plural = _('Banner Images')

    def __str__(self):
        return str(self.token_id)


class ChargePerKilometer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    charge = models.DecimalField(default=0, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'general_charge_per_kilometer'
        verbose_name = _('charge per kilometer')
        verbose_name_plural = _('charges per kilometer')

    def __unicode__(self):
        return str(self.id)


class Faq(BaseModel):
    question = models.CharField(max_length=128)
    answer = models.TextField()

    class Meta:
        db_table = 'frequently_asked_questions'
        verbose_name = _('Frequently Asked Question')
        verbose_name_plural = _('Frequently Asked Questions')

    def __str__(self):
        return f"{self.question}"


class Help(BaseModel):
    title = models.CharField(max_length=128)
    video = models.FileField(upload_to='delivery_agents/help')
    youtube_id = models.CharField(max_length=128)

    class Meta:
        db_table = 'help'
        verbose_name = _('Help')
        verbose_name_plural = _('Helps')

    def __str__(self):
        return f"{self.title}"

