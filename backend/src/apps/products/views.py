from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from src.apps.users.permissions import IsProducer, IsProducerOrReadOnly

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available', 'producer']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'stock_quantity']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsProducer()]
        return [permissions.AllowAny()]

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        # Only producer who owns the product can edit/delete
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsProducer()]
        return [permissions.AllowAny()]
    
    def perform_update(self, serializer):
        # Ensure only owner can update
        if serializer.instance.producer != self.request.user:
            self.permission_denied(self.request)
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.producer != self.request.user:
            self.permission_denied(self.request)
        instance.delete()