from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.views.generic.base import TemplateView

from store.views import index
from shop import settings

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('boutique/', include('store.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Serve media files in production using Render's disk storage
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
