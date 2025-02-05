import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from shop import settings
from store.models import Product, Cart, Order  # import product

stripe.api_key = settings.STRIPE_API_KEY

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
    order, created = Order.objects.get_or_create(user=user, ordered=False,product=product) # Get or create order

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
        cart.delete()
    
    return redirect("index")


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'store/cart.html', context={"cart": cart, "orders": cart.orders.all()})


YOUR_DOMAIN = 'http://localhost:8000'
def create_checkout_session(request):
    try:
        # Create a checkout session
        checkout_session = stripe.checkout.Session.create(
            locale="fr",
            payment_method_types=['card'],  # Only card payments
            line_items=[
                {
                    'price_data': {  # Corrected key
                        'currency': 'usd',
                        'product_data': {
                            'name': 'T-Shirt',  # Use real product name
                        },
                        'unit_amount': 2000,  # Amount in cents ($20.00)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/index/',  # Corrected URL
            cancel_url=YOUR_DOMAIN + '/index/',
        )

        # Redirect to Stripe checkout page
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  # Return a JSON response on error