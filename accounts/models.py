from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from iso3166 import countries

class CustomUserManager(BaseUserManager):
    # Custom manager for creating users and superusers without a username field
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)  # Encrypt password
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
    # Custom user model without a username field, using email instead
    username = None
    email = models.EmailField(max_length=240, unique=True)
    stripe_id = models.CharField(max_length=240, blank=True)

    # Mandatory fields for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

ADDRESS_FORMAT = """
{name}
{address_1}
{address_2}
{city}, {postal_code}
{country}
"""

class ShippingAddress(models.Model):
    user = models.ForeignKey(Shopper, on_delete=models.CASCADE, related_name="addresses") #user can have multiple shipping addresses
    name = models.CharField(max_length=240)
    address_1 = models.CharField(max_length=1024, help_text="Nom de rue et numéro")
    address_2 = models.CharField(max_length=1024, help_text="Bâtiment, étage, appartement, etc.", blank=True, null=True)
    city = models.CharField(max_length=240)
    postal_code = models.CharField(max_length=12)
    # liste de tuple avec en 1er deux lettres (bd) et après le pays
    country = models.CharField(max_length=2, choices=[(c.alpha2.lower(), c.name) for c in countries])

    def __str__(self):
        data = self.__dict__.copy()
        data.update(country=self.get_country_display().upper()) # get the country name from the country code
        """
        utiliser le unpacking pour afficher les infos de l'adresse dans le format défini
        strip("\n") pour enlever les retours à la ligne en trop
        """
        return ADDRESS_FORMAT.format(**data).strip("\n")
    