from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
"""
Product
- name
- price
- available
- description
- images
- others variants
"""
class Variant(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)
    variants = models.ManyToManyField("self", blank=True, symmetrical=False)

    def __str__(self):
        return self.name

