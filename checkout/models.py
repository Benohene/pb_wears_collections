from products.models import Product
import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings

# Create your models here.

class Order(models.Model):
    # The Order model is used to store the order information
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, blank=False)
    emal = models.EmailField(max_length=254, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=80, blank=False)
    street_address2 = models.CharField(max_length=80, blank=False)
    region = models.CharField(max_length=80, blank=False)
    date = models.DateField(auto_now=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    
    def _generate_order_number(self):
        # Generate a random, unique order number using UUID
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        # Update grand total each time a line item is added, accounting for delivery costs.
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()
    
    def save(self, *args, **kwargs):
        # Override the original save method to set the order number if it hasn't been set already.
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.order_number
    

class OrderLineItem(models.Model):
    # The OrderLineItem model is used to store the line item information
    order = models.ForeignKey(Order, blank=False, null=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # S, M, L, XL
    quantity = models.IntegerField(blank=False)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, editable=False)
    
    def save(self, *args, **kwargs):
        # Override the original save method to set the lineitem total and update the order total.
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'