from django.urls import path
from .views import DashboardView, OrderDetailView

urlpatterns= [
    path('dashboard/', DashboardView.as_view(), name= 'dashboard'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name= 'order-detail'),
]