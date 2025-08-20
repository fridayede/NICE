from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, related_name="product_cart_items", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    
class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, related_name="orders", on_delete=models.CASCADE)
    total_price = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class OrderItem(models.Model):
    product =  models.ForeignKey(Product, related_name="product_order_items", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="order_item", on_delete=models.CASCADE)
    total_price = models.DecimalField( max_digits=10, decimal_places=2)
    paid = models.BooleanField()
    status =models.CharField( max_length=250)
    quantity = models.PositiveIntegerField()