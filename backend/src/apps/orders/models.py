from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from src.apps.products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    consumer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        limit_choices_to={'user_type': 'consumer'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Shipping info (can be denormalized from user profile)
    delivery_address = models.TextField()
    phone_number = models.CharField(max_length=15)  # copy from consumer at order time
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['consumer', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Order {self.id} - {self.consumer.phone_number} - {self.status}"
    
    def update_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of product price
    
    class Meta:
        unique_together = ('order', 'product')  # prevent duplicate product in same order
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
    
    @property
    def subtotal(self):
        return self.quantity * self.price_at_time