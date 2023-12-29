import uuid
from decimal import Decimal
from versatileimagefield.fields import VersatileImageField
#django
from django.db import models
from django.urls import reverse
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
#local
from main.models import BaseModel


STATUS_CHOICES = (
    ('active','active'),
    ('disabled','disabled'),
)


class Category(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    image = VersatileImageField('Image',upload_to='products/categories/', blank=True,null=True)
    icon_name = models.CharField(max_length=12, default="home")

    def get_image(self):
        if self.image:
            try:
                image = self.image.crop['400x400'].url
            except:
                image = self.image.url
        else:
            image = ''
        return image

    def dashboard_image(self):
        if self.image:
            try:
                image = self.image.crop['100x100'].url
            except:
                image = self.image.url
        else:
            image = ''
        return image
        
    class Meta:
        db_table = 'product_category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('name',)      
    
    def __str__(self): 
        return self.name


class SubCategory(BaseModel):
    name = models.CharField(max_length=128)
    category = models.ForeignKey("products.Category",limit_choices_to={'is_deleted': False},blank=True,null=True,on_delete=models.CASCADE)
    image = VersatileImageField('Image',upload_to='products/sub_categories/',blank=True,null=True)
    icon_name = models.CharField(max_length=12, default="home")

    def get_image(self):
        if self.image:
            image = self.image.crop['250x250'].url
        else:
            image = ''
        return image
        
    def dashboard_image(self):
        if self.image:
            try:
                image = self.image.crop['100x100'].url
            except:
                image = self.image.url
        else:
            image = ''
        return image
    
    class Meta:
        db_table = 'product_sub_category'
        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')
        ordering = ('name',)      
    
    def __str__(self): 
        return self.name


class MetaKeyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'products_meta_keyword'
        verbose_name = _('Product Meta keyword')
        verbose_name_plural = _('Product Meta keywords')
        ordering = ('name',)

    def __str__(self):
        return str(self.name)


class Product(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True,null=True)
    featured_image = VersatileImageField('Featured Image', upload_to='products/featured_images', blank=True, null=True)
    image = VersatileImageField('Image', upload_to='products/images', blank=True, null=True)
    category = models.ForeignKey("products.Category", limit_choices_to={'is_deleted': False}, blank=True, null=True, on_delete=models.CASCADE)
    sub_category = models.ForeignKey("products.SubCategory", limit_choices_to={'is_deleted': False}, blank=True, null=True, on_delete=models.CASCADE)

    gst = models.PositiveIntegerField(null=True, blank=True)
    
    meta_keyword_description = models.TextField(null=True, blank=True)
    meta_keyword = models.ManyToManyField("products.MetaKeyword",related_name="meta_keyword", blank=True)

    status = models.CharField(choices=STATUS_CHOICES, max_length=128, default="active")

    is_variants = models.BooleanField(default=False)

    def get_featured_image(self):
        if self.featured_image:
            try:
                image = self.featured_image.crop['400x400'].url
            except:
                image = self.featured_image.url
        else:
            image = ''
        return image

    def get_image(self):
        if self.image:
            try:
                image = self.image.crop['400x400'].url
            except:
                image = self.image.url
        elif self.featured_image:
            try:
                image = self.featured_image.crop['400x400'].url
            except:
                image = self.featured_image.url
        else:
            image = ''
        return image

    def dashboard_featured_image(self):
        if self.featured_image:
            try:
                image = self.featured_image.crop['100x100'].url
            except:
                image = self.featured_image.url
        else:
            image = ''
        return image

    def dashboard_image(self):
        if self.image:
            try:
                image = self.image.crop['100x100'].url
            except:
                image = self.image.url
        elif self.featured_image:
            try:
                image = self.featured_image.crop['100x100'].url
            except:
                image = self.featured_image.url
        else:
            image = ''
        return image

    def default_variant(self):
        variant = ''
        if ProductVariant.objects.filter(product=self, is_deleted=False).exists():
            if ProductVariant.objects.filter(product=self, is_deleted=False, stock__gte=1, is_default=True).exists():
                variant = ProductVariant.objects.filter(product=self, is_deleted=False, stock__gte=1, is_default=True)[0]
            elif ProductVariant.objects.filter(product=self, is_deleted=False, stock__gte=1).exists():
                variant = ProductVariant.objects.filter(product=self, is_deleted=False, stock__gte=1)[0]
            elif ProductVariant.objects.filter(product=self, is_deleted=False, is_default=True).exists():
                variant = ProductVariant.objects.filter(product=self, is_deleted=False, is_default=True)[0]
            else:
                variant = ProductVariant.objects.filter(product=self, is_deleted=False)[0]
        return variant

    class Meta:
        db_table = 'products_product'
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('name',)  
        
    def __str__(self):
        return self.name 


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128, blank=True, null=True)
    product = models.ForeignKey("products.Product", limit_choices_to={'is_deleted': False}, blank=True, null=True, on_delete=models.CASCADE)
    # image = VersatileImageField('Variant Image', upload_to='products/images', blank=True, null=True)

    mrp = models.DecimalField(decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    stock = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])

    out_of_stock_date = models.DateTimeField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    def get_image(self):
        if self.image:
            try:
                image = self.image.crop['250x250'].url
            except:
                image = self.image.url
        else:
            image = ''
        return image
        
    class Meta:
        db_table = 'product_variant'
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product Variants')
        ordering = ('product',)  

    def full_name(self):
        if self.title:
            return self.product.name + " " + self.title
        else:
            return self.product.name
        
    def __str__(self):
        return str(self.product.name +" - " + str(self.title)) 


# class ProductVariantImages(models.Model):
#     product_variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE,null=True,blank=True)
#     image = VersatileImageField('Variant Images', upload_to='products/images', blank=True, null=True)

#     def get_image(self):
#         if self.image:
#             image = self.image.crop['250x250'].url
#         else:
#             image = ''
#         return image

#     class Meta:
#         db_table = 'product_variant_image'
#         verbose_name = _('Product Variant Image')
#         verbose_name_plural = _('Product Variant Images')
#         ordering = ('product_variant',)

#     def __str__(self):
#         return str(self.id)


