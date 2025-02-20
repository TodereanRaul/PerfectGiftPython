import stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from shop import settings
from store.models import Product, Cart, Order  # import product
import json

YOUR_DOMAIN = 'http://localhost:8000'

stripe.api_key = settings.STRIPE_API_KEY

def index(request):
    products = Product.objects.all()

    return render(request, 'store/index.html', context={"products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        comment = request.POST.get("comment")
        if comment:
            product.user_comment = comment  # Sauvegarde du commentaire
            product.save()
            return redirect("product", slug=product.slug)  # Rafraîchit la page
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


def create_checkout_session(request):
    cart = request.user.cart
    line_items = [{"price": order.product.stripe_id,
                   "quantity": order.quantity} for order in cart.orders.all()]

    try:
        # Create a checkout session
        checkout_session = stripe.checkout.Session.create(
            locale="fr",
            payment_method_types=['card'],  # Only card payments
            line_items=line_items,
            mode='payment',
            success_url = YOUR_DOMAIN + reverse('checkout-success'),
            cancel_url=YOUR_DOMAIN + '/',
        )

        # Redirect to Stripe checkout page
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  # Return a JSON response on error

def checkout_success(request):
    return render(request, 'store/success.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object  # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!')
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object  # contains a stripe.PaymentMethod
        print('PaymentMethod was attached to a Customer!')
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)