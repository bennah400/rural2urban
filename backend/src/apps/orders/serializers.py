from rest_framework import serializers
from .models import Order, OrderItem
from src.apps.products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_time', 'subtotal']
        read_only_fields = ['price_at_time', 'subtotal']
    
    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']
        if quantity > product.stock_quantity:
            raise serializers.ValidationError(
                f"Only {product.stock_quantity} items available for {product.name}"
            )
        return attrs
    
    def create(self, validated_data):
        product = validated_data['product']
        validated_data['price_at_time'] = product.price
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=False, required=True)
    consumer_phone = serializers.CharField(source='consumer.phone_number', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'consumer', 'consumer_phone', 'created_at', 'updated_at',
            'status', 'total_amount', 'delivery_address', 'phone_number', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_amount', 'status', 'consumer']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['consumer'] = self.context['request'].user
        if 'phone_number' not in validated_data or not validated_data['phone_number']:
            validated_data['phone_number'] = str(self.context['request'].user.phone_number)
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            # Deduct stock
            product.stock_quantity -= quantity
            product.save(update_fields=['stock_quantity'])
            # Create OrderItem with price_at_time from product
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_time=product.price  # <-- fix here
            )

        order.update_total()
        return order