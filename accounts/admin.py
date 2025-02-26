from django.contrib import admin
from accounts.models import ShippingAddress, Shopper

# Register your models here.
admin.site.register(Shopper)
admin.site.register(ShippingAddress)