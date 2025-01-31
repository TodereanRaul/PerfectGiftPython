from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from store.views import index

from shop import settings

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #this allows to show img in local dev mode -- NEEDS TO BE CHANGED WHEN LIVE
