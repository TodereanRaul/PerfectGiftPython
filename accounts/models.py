from django.contrib.auth.models import AbstractUser
from django.db import models

class Shopper(AbstractUser):
    username = None
    email = models.EmailField(max_length=240,unique=True)

    USERNAME_FIELD = 'email'
    # mandatrory fields for login
    REQUIRED_FIELDS = []
