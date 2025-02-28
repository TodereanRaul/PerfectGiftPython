from http.client import HTTPS_PORT
from importlib.metadata import metadata
from pprint import pprint

from django.forms import modelformset_factory
import stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import stripe.error

from accounts.models import ShippingAddress, Shopper
from shop import settings
from store.forms import OrderForm
from store.models import Product, Cart, Order  # import product

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
    orderes = Order.objects.filter(user=request.user, ordered=False) # get orders for the user
    if orderes.count() == 0:
        return redirect("index")
    OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0) # forms for the orders - extra=0 to not add new forms - form=OrderForm to use the form we created
    formset = OrderFormSet(queryset=orderes) # queryset to get the orders
    
    # if the form is valid, save the form
    if request.method == "POST":
        formset = OrderFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('cart')

    return render(request, 'store/cart.html', context={"forms": formset})



def create_checkout_session(request):
    user  = request.user

    # check if user has a stripe id, if not create one
    if not user.stripe_id:
        try:
            customer = stripe.Customer.create(email=user.email,
                                              name=user.username if user.username else user.email)
            user.stripe_id = customer['id']
            user.save()
        except stripe.error.StripeError as e:
            # Display a very generic error to the user
            print(f"Erreur Stripe : {e}")
            return JsonResponse({"error": str(e)}, status=500)

    cart = user.cart

    line_items = [{"price": order.product.stripe_id,
                   "quantity": order.quantity} for order in cart.orders.all()]

    try:
        # Create a checkout session
        checkout_session = stripe.checkout.Session.create(
            locale="fr",
            shipping_address_collection={
                'allowed_countries': ['BE']
            },
            customer=user.stripe_id,
            payment_method_types=['card'],  
            line_items=line_items,
            mode='payment',
            success_url = YOUR_DOMAIN + reverse('checkout-success'),
            cancel_url=YOUR_DOMAIN + '/',
            metadata={
                "user_email": request.user.email
            }
        )

        
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500) 

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

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        # Object is a checkout.session
        data = event['data']['object']

        try:
            user = get_object_or_404(Shopper, email=data['customer_details']['email'])
        except KeyError as e:
            return HttpResponse("Invalid user email", status=404)
        
        complete_order(data=data, user=user)
        save_shipping_address(data=data, user=user)
        return HttpResponse(status=200)

    return HttpResponse(status=200)


def complete_order(data, user):
    user.stripe_id = data['customer']
    user.cart.order_ok()
    user.save()
    return HttpResponse(status=200)

def save_shipping_address(data, user):
    """
    "collected_information": {
    "shipping_details": {
      "address": {
        "city": "Saint-Josse-ten-Noode",
        "country": "BE",
        "line1": "Rue de Brabant",
        "line2": null,
        "postal_code": "1234",
        "state": null
      },
      "name": "maison"
    }
    """

    try:
        address = data["shipping_details"]["address"]
        name = data["shipping_details"]["name"]
        city = address["city"]
        country = address["country"]
        line1 = address["line1"]
        line2 = address["line2"]
        postal_code = address["postal_code"]
    except KeyError:
        return HttpResponse(status=400)

    ShippingAddress.objects.get_or_create(user=user,
                                          name=name,
                                          city=city,
                                          country=country.lower(),
                                          address_1=line1,
                                          address_2=line2 or " ",
                                          postal_code=postal_code)
    return HttpResponse(status=200)