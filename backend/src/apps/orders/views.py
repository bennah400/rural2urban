from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer
from src.apps.users.permissions import IsConsumer

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'consumer':
            return Order.objects.filter(consumer=user)
        elif user.user_type == 'producer':
            # Producers see orders that contain their products
            return Order.objects.filter(items__product__producer=user).distinct()
        return Order.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user)

class OrderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'consumer':
            return Order.objects.filter(consumer=user)
        elif user.user_type == 'producer':
            return Order.objects.filter(items__product__producer=user).distinct()
        return Order.objects.none()
    
    def update(self, request, *args, **kwargs):
        # Only allow status updates, not full order changes
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if 'status' in request.data:
            instance.status = request.data['status']
            instance.save(update_fields=['status'])
            return Response(self.get_serializer(instance).data)
        return Response({"detail": "Only status updates allowed."}, status=status.HTTP_400_BAD_REQUEST)