from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import OrderView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customer.urls')),
    path('restaurant/', include('restorant.urls')),
    path('accounts/', include('users.urls')),
    path('order/', OrderView.as_view(), name= 'order'),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
