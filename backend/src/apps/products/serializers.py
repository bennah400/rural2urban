from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    producer_phone = serializers.CharField(source='producer.phone_number', read_only=True)
    producer_name = serializers.CharField(source='producer.full_name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'producer', 'producer_phone', 'producer_name',
            'name', 'description', 'price', 'stock_quantity',
            'image', 'category', 'is_available', 'created_at', 'updated_at', 'in_stock'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'producer']
    
    def create(self, validated_data):
        # Auto-set producer to logged-in user
        validated_data['producer'] = self.context['request'].user
        return super().create(validated_data)