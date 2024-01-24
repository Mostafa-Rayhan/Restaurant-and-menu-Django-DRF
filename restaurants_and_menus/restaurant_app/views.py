
from django.conf import settings
from rest_framework import generics
from .models import Restaurant, Menu, MenuItem, Order
from .serializers import RestaurantSerializer, MenuSerializer, MenuItemSerializer, OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe

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
    
# Stripe API Integration
class PaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_price * 100),  # amount in cents
            currency='usd',
            metadata={'order_id': order.id},
        )

        order.stripe_payment_intent = intent.client_secret
        order.save()

        return Response({'client_secret': intent.client_secret})
