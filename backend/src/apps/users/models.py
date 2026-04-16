# apps/users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    """Custom manager for CustomUser where phone_number is the unique identifier."""
    
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Create and save a regular user.
        Required: phone_number.
        """
        if not phone_number:
            raise ValueError('The Phone Number must be set')
        
        # Normalize phone number (remove spaces, ensure format - we'll do more later)
        phone_number = self.normalize_phone_number(phone_number)
        
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # for OTP-based login
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Create and save a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(phone_number, password, **extra_fields)
    
    @staticmethod
    def normalize_phone_number(phone):
        """Basic normalization – strip whitespace. For production, use phonenumbers library."""
        return phone.strip()

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model using phone number as login.
    Replaces Django's default username-based model.
    """
    # Phone number – unique identifier for login and M-Pesa
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+254XXXXXXXXX'. Up to 15 digits."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True,
        help_text="Required. Used for login and M-Pesa transactions."
    )
    
    # Optional fields
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    # Status flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Rural2Urban specific: user type
    USER_TYPE_CHOICES = (
        ('producer', 'Rural Producer'),
        ('consumer', 'Urban Consumer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='consumer')
    
    # Producer-specific fields (nullable for consumers)
    farm_name = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, help_text="e.g., county or village")
    
    # Consumer-specific fields
    delivery_address = models.TextField(blank=True, null=True)
    
    # Required by Django
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []   # phone_number is already required, no other mandatory fields for createsuperuser
    
    objects = UserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.phone_number} - {self.get_user_type_display()}"
    
    def get_full_name(self):
        return self.full_name or str(self.phone_number)
    
    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else str(self.phone_number)