from http.client import HTTPS_PORT
from importlib.metadata import metadata
from pprint import pprint

import stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Shopper
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
            metadata={
                "user_email": request.user.email
            }
        )

        # Redirect to Stripe checkout page
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  # Return a JSON response on error

endpoint_secret = 'whsec_517e4430b4ef6cd82c3dd1bc5875745dc3eed84b823491b73760bb05adf8288e'

def checkout_success(request):
    return render(request, 'store/success.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print(f"Payload invalide : {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"Signature invalide : {str(e)}")
        return HttpResponse(status=400)

    # Logging pour vérifier les données reçues
    print(f"Événement reçu : {event.type}")
    pprint(event)

    # Gérer l'événement checkout.session.completed
    if event.type == 'checkout.session.completed':
        data = event['data']['object']
        return complete_order(data)

    return HttpResponse(status=200)


def complete_order(data):
    try:
        # Récupérer l'email depuis les métadonnées
        user_email = data['metadata'].get('user_email')
        if not user_email:
            raise KeyError("Email manquant dans les métadonnées")
    except KeyError as e:
        print(f"Erreur: {str(e)}")
        return HttpResponse("Invalid user email", status=404)

    # Récupérer l'utilisateur associé à l'email
    user = get_object_or_404(Shopper, email=user_email)

    # Vérifier et compléter la commande
    if not hasattr(user, 'cart'):
        print("Erreur: Aucun panier associé à cet utilisateur")
        return HttpResponse("Cart not found for user", status=404)

    user.cart.ordered = True
    user.cart.ordered_date = timezone.now()
    user.cart.save()
    return HttpResponse(status=200)
