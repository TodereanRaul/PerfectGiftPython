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
class Product (models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True) #Allow admin to register items without description
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True) #Stores Images in folder named 'products'
    variantIds = ArrayField(models.IntegerField(), blank=True)

