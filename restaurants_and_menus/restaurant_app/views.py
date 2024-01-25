
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant, Menu, MenuItem, Order
from .serializers import RestaurantSerializer, MenuSerializer, MenuItemSerializer, OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe

class RestaurantListCreateView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Restaurant.objects.filter(owner=self.request.user)
        else:
            return Restaurant.objects.none()

class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Restaurant.objects.filter(owner=self.request.user)
        else:
            return Restaurant.objects.none()

class MenuListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Menu.objects.filter(restaurant__owner=self.request.user)
        else:
            return Menu.objects.none()

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Menu.objects.filter(restaurant__owner=self.request.user)
        else:
            return Menu.objects.none()

class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MenuItem.objects.filter(menu__restaurant__owner=self.request.user)
        else:
            return MenuItem.objects.none()

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MenuItem.objects.filter(menu__restaurant__owner=self.request.user)
        else:
            return MenuItem.objects.none()

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.none()

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.none()
    
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
