import uuid

from attr.validators import min_len
from django.contrib.auth import get_user_model
from django.db import models

from store.models import Product, ProductVariation

# Create your models here.
User=get_user_model()
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cart_items')
    productVariation=models.ForeignKey(ProductVariation, on_delete=models.CASCADE,related_name='cart_items')
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f'{self.user.name} - {self.productVariation.product.name}'




class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='shipping_address')
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    address_line_1 = models.CharField(max_length=255, verbose_name="Address Line 1")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address Line 2")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State")
    pin_code = models.CharField(max_length=6, verbose_name="Pin Code")  # Indian PIN codes are 6 digits
    phone_number = models.CharField(max_length=10, verbose_name="Phone Number")  # Assuming Indian phone numbers
    email = models.EmailField(blank=True, null=True, verbose_name="Email")

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.state}"


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    address=models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.name}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_item')
    product_variation=models.ForeignKey(ProductVariation, on_delete=models.CASCADE,related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.quantity} x {self.product_variation.product.name} in Order #{self.order.id}"


class OrderPayment(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status=models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES, default='pending')
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order #{self.order.id}"


