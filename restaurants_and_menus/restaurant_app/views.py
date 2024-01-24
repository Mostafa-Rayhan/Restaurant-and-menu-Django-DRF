# restaurant_app/views.py

from rest_framework import generics
from .models import Restaurant, Menu, MenuItem, Order
from .serializers import RestaurantSerializer, MenuSerializer, MenuItemSerializer, OrderSerializer

class RestaurantListCreateView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)

class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)

class MenuListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(restaurant__owner=self.request.user)

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(restaurant__owner=self.request.user)

class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.filter(menu__restaurant__owner=self.request.user)

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        return MenuItem.objects.filter(menu__restaurant__owner=self.request.user)

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
