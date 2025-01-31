from django.urls import reverse
from django.utils.text import slugify
from django.db import models

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
