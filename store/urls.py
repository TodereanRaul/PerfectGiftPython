from django.urls import path

from store.views import about, cart, contact, delete_cart, product_detail, add_to_cart, create_checkout_session, \
    checkout_success, product_list, stripe_webhook

app_name = "store"

urlpatterns = [
    path('about', about, name="about"),
    path('contact/', contact, name="contact"),
    path('product-list', product_list, name="product-list"),
    path('cart', cart, name="cart"),
    path('stripe-webhook/', stripe_webhook, name="stripe-webhook"),
    path('store/success', checkout_success, name="checkout-success"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('cart/create_checkout_session/', create_checkout_session, name="create_checkout_session"),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name="add-to-cart"),
]

https://github.com/TodereanRaul/PerfectGiftPython/commit/a25e9ea8c39503764e745051921c0be5abad7e03
