from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password) #encrypt password
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class Shopper(AbstractUser):
    username = None
    email = models.EmailField(max_length=240,unique=True)

    USERNAME_FIELD = 'email'
    # mandatrory fields for login
    REQUIRED_FIELDS = []
    objects = CustomUserManager()