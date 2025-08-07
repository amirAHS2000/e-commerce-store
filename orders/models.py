from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models import Sum, F

from decimal import Decimal

from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart for {self.user.username} (Active: {self.is_active})"
    
    # def get_total_price(self):
    #     total = Decimal('0.00')
    #     for item in self.items.all():
    #         total += item.get_total_price()
    #     return total
    
    # Optimized version for get_total_price function (using aggregation)
    def get_total_price(self):
        total = self.items.aggregate(total_price=Sum(F('quantity') * F('price'), output_field=models.DecimalField()))['total_price']
        return total if total is not None else Decimal('0.00')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product')
        ]
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"
    
    @property
    def get_total_price(self):
        return self.quantity * self.price


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # TODO: seperate out the "Address" model later
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - Status: {self.get_status_display()}"

    # def calculate_total_price(self):
    #     total = Decimal('0.00')
    #     for item in self.items.all():
    #         total += item.get_total_price()
    #     return total
    
    # Optimized version of above function
    def calculate_total_price(self):
        total = self.items.aggregate(total_price=Sum(F('quantity') * F('price'), output_field=models.DecimalField()))['total_price']
        return total if total is not None else Decimal('0.00')

    # def save(self, *args, **kwargs):
        # self.total_price = self.calculate_total_price()
        # super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'product'], name='unique_order_product')
        ]
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Deleted Product'} in Order {self.order.id}"

    @property
    def get_total_price(self):
        return self.quantity * self.price
