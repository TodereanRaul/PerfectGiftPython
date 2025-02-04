from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from store.models import Product, Cart, Order  # import product

def index(request):
    products = Product.objects.all()

    return render(request, 'store/index.html', context={"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product-detail.html', context={"product": product})

def add_to_cart(request, slug):
    user = request.user # get user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)  # Get or create cart
    order, created = Order.objects.get_or_create(user=user, product=product) # Get or create order

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("product", kwargs={"slug": slug}))

def delete_cart(request):
    cart = getattr(request.user, "cart", None)  
    
    if cart:
        cart.orders.all().delete()
        cart.delete()
    
    return redirect("index")


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'store/cart.html', context={"cart": cart, "orders": cart.orders.all()})