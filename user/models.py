from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .custom_manager import CustomUserManager

from utils.user_related import user_type

from utils.user_related import validate_bd_phone_number


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.CharField(max_length=10, choices=user_type, default='customer')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    address= models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True, validators=[validate_bd_phone_number])
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    
    def save(self, *args, **kwargs):
        if not self.phone_number:
            self.phone_number = None
        super().save(*args, **kwargs)