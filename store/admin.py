from django.contrib import admin
from store.models import Product, ProductImage,Order, Cart

# Inline pour afficher les images secondaires dans la page du produit
class ProductImageInline(admin.TabularInline):  # Ou admin.StackedInline pour un affichage vertical
    model = ProductImage
    extra = 1  # Nombre de champs vides affichés pour ajouter de nouvelles images

# Configuration de l'administration pour le modèle Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')  # Colonnes affichées dans la liste des produits
    inlines = [ProductImageInline]  # Ajouter l'inline pour les images secondaires

# Enregistrement des modèles dans l'administration
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Cart)