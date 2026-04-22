from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Define the upload path function BEFORE the Product class
def product_image_upload_path(instance, filename):
    """Generate a dynamic upload path: media/product_images/producer_<id>/<filename>"""
    return f'product_images/producer_{instance.producer.id}/{filename}'

class Product(models.Model):
    # Relationships
    producer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        limit_choices_to={'user_type': 'producer'}  # only producers can own products
    )
    
    # Basic info
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    
    # Optional fields
    image = models.ImageField(
        upload_to=product_image_upload_path,   #  changed from 'products/' to function
        blank=True,
        null=True
    )   
    category = models.CharField(max_length=100, blank=True, default='General')
    
    # Status
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['producer', 'is_available']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.producer.phone_number}"
    
    @property
    def in_stock(self):
        return self.stock_quantity > 0 and self.is_available