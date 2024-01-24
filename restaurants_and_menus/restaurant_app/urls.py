
from django.urls import path
from .views import (
    RestaurantListCreateView, RestaurantDetailView,
    MenuListCreateView, MenuDetailView,
    MenuItemListCreateView, MenuItemDetailView,
    OrderListCreateView, OrderDetailView,
    PaymentIntentView,
)

urlpatterns = [
    path('restaurants/', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),

    path('menus/', MenuListCreateView.as_view(), name='menu-list-create'),
    path('menus/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),

    path('menu-items/', MenuItemListCreateView.as_view(), name='menu-item-list-create'),
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menu-item-detail'),

    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('payment-intent/', PaymentIntentView.as_view(), name='payment-intent'),
]
