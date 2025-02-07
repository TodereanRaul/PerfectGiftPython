from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db import models
from shop.settings import AUTH_USER_MODEL


class Variant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Slug généré automatiquement si vide
    price = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)
    description = RichTextField(blank=True)  # RichText pour mise en forme
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)  # Image principale
    variants = models.ManyToManyField("self", blank=True, symmetrical=False)
    user_comment = models.TextField(blank=True, null=True)
    stripe_id = models.CharField(max_length=90, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Générer le slug automatiquement
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images", blank=True, null=True)

    def __str__(self):
        return f"Image de {self.product.name}"

# (Order)
class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) #user relie a plusieurs articles grace a foreignKey() - on_delete-> si user deleted from db if will erase his stored products
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) # quantity of one item in the cart
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

# (Cart)
class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)


    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        self.orders.clear()
        super().delete(*args, **kwargs)