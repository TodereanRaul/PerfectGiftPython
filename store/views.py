from django.shortcuts import render, get_object_or_404

from store.models import Product #import product

def index(request):
    products = Product.objects.all()

    return render(request, 'store/index.html', context={"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product-detail.html', context={"product": product})
