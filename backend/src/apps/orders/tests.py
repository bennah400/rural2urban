from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from src.apps.products.models import Product

User = get_user_model()

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.consumer = User.objects.create_user(
            phone_number='+254711111111', password='pass', user_type='consumer',
            full_name='Test Consumer', delivery_address='123 Nairobi St'
        )
        self.producer = User.objects.create_user(
            phone_number='+254722222222', password='pass', user_type='producer',
            full_name='Test Producer'
        )
        self.product = Product.objects.create(
            producer=self.producer, name='Maize', description='Fresh', price=50.00, stock_quantity=100
        )
        self.order_url = reverse('order-list-create')
        
    def test_consumer_can_create_order(self):
        self.client.force_authenticate(user=self.consumer)
        data = {
            'delivery_address': '123 Nairobi St',
            'phone_number': '+254711111111',
            'items': [{'product': self.product.id, 'quantity': 2}]
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_amount'], '100.00')
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 98)
    
    def test_producer_cannot_create_order(self):
        self.client.force_authenticate(user=self.producer)
        data = {'delivery_address': 'Farm', 'items': []}
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_consumer_sees_own_orders(self):
        self.client.force_authenticate(user=self.consumer)
        # Create an order
        data = {'delivery_address': 'Nairobi', 'items': [{'product': self.product.id, 'quantity': 1}]}
        self.client.post(self.order_url, data, format='json')
        # List orders
        response = self.client.get(self.order_url)
        self.assertEqual(len(response.data), 1)