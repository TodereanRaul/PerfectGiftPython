from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from shop.settings import AUTH_USER_MODEL


class Variant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Ensure uniqueness & allow auto-generation
    price = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)
    variants = models.ManyToManyField("self", blank=True, symmetrical=False)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's empty
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # obtenir à partir du nom d'url ('product') et des infos passés à l'url ('slug') l'adresse vers la page du produit
    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

# (Order)
class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) #user relie a plusieurs articles grace a foreignKey() - on_delete-> si user deleted from db if will erase his stored products
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) # quantity of one item in the cart
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

# (Cart)
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

