

from django.urls import path
from .views import *
urlpatterns = [
    path('cart/',CartView.as_view() , name='orders'),
    path('shipping-address/',ShippingAddressView.as_view() , name='shipping-address'),
    path('orders/',OrdersView.as_view() , name='orders'),
]