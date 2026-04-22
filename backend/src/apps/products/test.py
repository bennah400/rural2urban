from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.producer = User.objects.create_user(
            phone_number='+254711111111',
            password='pass123',
            user_type='producer',
            full_name='Test Producer'
        )
        self.consumer = User.objects.create_user(
            phone_number='+254722222222',
            password='pass123',
            user_type='consumer'
        )
        self.product_data = {
            'name': 'Fresh Tomatoes',
            'description': 'Organic farm tomatoes',
            'price': '150.00',
            'stock_quantity': 100,
            'category': 'Vegetables'
        }
    
    def test_producer_can_create_product(self):
        self.client.force_authenticate(user=self.producer)
        response = self.client.post(reverse('product-list-create'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().producer, self.producer)
    
    def test_consumer_cannot_create_product(self):
        self.client.force_authenticate(user=self.consumer)
        response = self.client.post(reverse('product-list-create'), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_can_list_products(self):
        Product.objects.create(producer=self.producer, **self.product_data)
        response = self.client.get(reverse('product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_producer_can_update_own_product(self):
        self.client.force_authenticate(user=self.producer)
        product = Product.objects.create(producer=self.producer, **self.product_data)
        url = reverse('product-detail', args=[product.id])
        response = self.client.patch(url, {'price': '200.00'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(float(product.price), 200.00)
    
    def test_product_image_optional(self):
        """Test product creation without image still works"""
        self.client.force_authenticate(user=self.producer)
        response = self.client.post(
            reverse('product-list-create'),
            self.product_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data.get('image'))