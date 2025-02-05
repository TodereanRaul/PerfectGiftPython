from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from store.views import cart, delete_cart, index, product_detail, add_to_cart, create_checkout_session
from accounts.views import signup, login_user
from accounts.views import signout

from shop import settings

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name="signup"),
    path('signout', signout, name="signout"),
    path('login', login_user, name="login"),
    path('cart', cart, name="cart"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('cart/create_checkout_session/', create_checkout_session, name="create_checkout_session"),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name="add-to-cart"),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #this allows to show img in local dev mode -- NEEDS TO BE CHANGED WHEN LIVE
