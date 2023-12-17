from __future__ import unicode_literals
import uuid
import datetime
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from main.models import BaseModel


ORDER_STATUS_CHOICES = (
    ('pending','Pending'),
    ('packed','Packed'),
    ('shipped','Shipped'),
    ('delivered','Delivered'),
    ('cancelled','Cancelled'),
    ('completed', 'Completed')
)

ORDER_PAYMENT_METHOD_CHOICES = (
    ('cash on delivery','Cash On Delivery'),
    ('online payment','Online Payment'),
)


class Order(BaseModel):
    order_id = models.CharField(max_length=128)
    billing_address = models.ForeignKey("customers.CustomerAddress", on_delete=models.CASCADE,blank=True,null=True)
    customer = models.ForeignKey("customers.Customer", limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    
    amount_payable = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    amount_paid = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    sub_total = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))]) 
    total_amount = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))]) 
    discount_amount = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))]) 
    delivery_charge = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))]) 
    suggestion = models.TextField(null=True,blank=True)
    
    status = models.CharField(max_length=128,choices=ORDER_STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=128,choices=ORDER_PAYMENT_METHOD_CHOICES)

    total_distance = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))]) 
    time_duration = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))]) 
    # payment = models.ForeignKey('payments.Payment', limit_choices_to={'is_deleted': False},blank=True,null=True,on_delete=models.CASCADE)
    
    # delivery_agent = models.ForeignKey('delivery_agents.DeliveryAgent', limit_choices_to={'is_deleted': False},on_delete=models.CASCADE,blank=True,null=True)
    delivery_date = models.DateTimeField(auto_now_add=True, blank=True,null=True)

    accepted_by_delivery_agent = models.BooleanField(default=False)
    rejected_by_delivery_agent = models.BooleanField(default=False)
    
    is_cancelled = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False)
    is_hand_over = models.BooleanField(default=False)

    def order_items(self):
        return OrderItem.objects.filter(order=self)

    def items_count(self):
        return OrderItem.objects.filter(order=self).count()

    class Meta:
        db_table = 'order'
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('-date_added',)
    
    def __str__(self): 
        return "%s - %s" %(str(self.customer.name),str(self.amount_payable))


class OrderItem(models.Model):
    order = models.ForeignKey("orders.Order", limit_choices_to={'is_deleted': False},on_delete=models.CASCADE)
    product_variant = models.ForeignKey("products.ProductVariant",on_delete=models.CASCADE,blank=True,null=True)
    qty = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    cost = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    price = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    tax = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    tax_amount = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    discount_amount = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    subtotal = models.DecimalField(default=0,decimal_places=2, max_digits=15,validators=[MinValueValidator(Decimal('0.00'))])
    
    is_deleted = models.BooleanField(default=False)
     
    class Meta:
        db_table = 'order_item'
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
         
    def taxable_amount(self):
        return str(self.subtotal) - str(self.tax_amount)     

    def quantity(self):
        return str(round(self.qty,0))     
    
    def __str__(self): 
        return "%s - %s" %(str(self.product_variant.title),str(self.qty)) 