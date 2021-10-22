from django.urls import path
from .views import IndexView, AboutView, OrderConfirmationView, MenuView, MenuSearchView, OrderPayConfirmationView

urlpatterns= [
    path('', IndexView.as_view(), name= 'index'),
    path('about/', AboutView.as_view(), name= 'about'),
    path('menu/', MenuView.as_view(), name= 'menu'),
    path('menu/search/', MenuSearchView.as_view(), name= 'menu-search'),
    path('order/<int:pk>/confirmation/', OrderConfirmationView.as_view(), name= 'order-confirmation'),
    path('order/payment-confirmation/', OrderPayConfirmationView.as_view(), name= 'payment-confirmation'),
]