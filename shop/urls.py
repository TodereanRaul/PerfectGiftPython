from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from store.views import index
from shop import settings

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('boutique/', include('store.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #this allows to show img in local dev mode -- NEEDS TO BE CHANGED WHEN LIVE
