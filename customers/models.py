import uuid
#Third party
from decimal import Decimal
from versatileimagefield.fields import VersatileImageField
#Django
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
#Local
from main.models import BaseModel


SAVE_ADDRESS_CHOICES = (
    ('home','Home'),
    ('office','Office'),
    ('other','Other'),
)


class Customer(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=12, blank=True, null=True)
    profile_pic = VersatileImageField('Profile Pics', upload_to='customers/profile_pics', blank=True, null=True)

    date_added = models.DateTimeField(db_index=True,auto_now_add=True,null=True)
    is_active = models.BooleanField(default=False) 
    is_deleted = models.BooleanField(default=False)   

    class Meta:
        db_table = 'customers'
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ('name',)

    def __str__(self):
        try:
            name = self.name + " - " + self.phone
        except:
            name = self.phone

        return name


class CustomerAddress(models.Model):
    customer = models.ForeignKey("customers.Customer", limit_choices_to={'is_deleted': False}, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=128)

    location = models.ForeignKey("general.Location", limit_choices_to={'is_deleted': False}, on_delete=models.CASCADE)
    landmark = models.CharField(max_length=128)
    house_flat_block_no = models.CharField(max_length=128, blank=True, null=True)
    save_as = models.CharField(max_length=128, choices=SAVE_ADDRESS_CHOICES, default="home")

    total_distance = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    total_duration = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])

    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'customer_address'
        verbose_name = _('Customer Address')
        verbose_name_plural = _('Customer Addresses')
        ordering = ('name',)

    def __str__(self):
        return str(self.name) + " - " + str(self.phone)


class Cart(BaseModel):
    customer = models.OneToOneField("customers.Customer", on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))], default=0.00)

    class Meta:
        db_table = 'customer_cart'
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ('customer', )

    def __str__(self):
        return self.customer.name


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey("customers.Cart", limit_choices_to={'is_deleted': False}, on_delete=models.CASCADE)
    product_variant = models.ForeignKey('products.ProductVariant', limit_choices_to={'is_deleted': False}, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.DecimalField(decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('1.00'))
    price = models.DecimalField(decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('1.00'))
    subtotal = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.00'))])
    
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'customer_cart_item'
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        ordering = ('-id', )

    def item_qty(self):
        if self.qty:
            return int(self.qty)
        else:
            return 1

    def __str__(self):
        return self.product_variant.product.name



