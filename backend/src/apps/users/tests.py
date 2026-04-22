from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user-register')  # name from urls.py
        self.valid_payload = {
            'phone_number': '+254712345678',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'full_name': 'John Mwangi',
            'email': 'john@example.com',
            'user_type': 'producer',
            'farm_name': 'Green Acres Farm',
            'location': 'Kiambu',
        }
    
    def test_register_user_success(self):
        """Test successful user registration returns 201 and JWT tokens"""
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        
        user_data = response.data['user']
        self.assertEqual(user_data['phone_number'], self.valid_payload['phone_number'])
        self.assertEqual(user_data['full_name'], self.valid_payload['full_name'])
        self.assertEqual(user_data['user_type'], self.valid_payload['user_type'])
        
        # Verify user exists in DB
        user = User.objects.get(phone_number=self.valid_payload['phone_number'])
        self.assertTrue(user.check_password(self.valid_payload['password']))
        self.assertEqual(user.full_name, self.valid_payload['full_name'])
    
    def test_register_duplicate_phone_number(self):
        """Test registration with existing phone number fails"""
        # Create first user
        self.client.post(self.register_url, self.valid_payload, format='json')
        
        # Try to register same phone number again
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
    
    def test_register_password_mismatch(self):
        """Test password and confirm password mismatch"""
        payload = self.valid_payload.copy()
        payload['password2'] = 'DifferentPass123!'
        
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)  # error on password field
    
    def test_register_weak_password(self):
        """Test weak password is rejected by Django validators"""
        payload = self.valid_payload.copy()
        payload['password'] = '1234'
        payload['password2'] = '1234'
        
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_register_missing_required_field(self):
        """Test missing phone_number (required) returns error"""
        payload = self.valid_payload.copy()
        del payload['phone_number']
        
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
    
    def test_register_invalid_phone_number_format(self):
        """Test invalid phone number format (not E.164)"""
        payload = self.valid_payload.copy()
        payload['phone_number'] = '0712345678'  # missing country code
        
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
    
    def test_register_duplicate_email(self):
        """Test duplicate email (if provided) is rejected"""
        # First registration
        self.client.post(self.register_url, self.valid_payload, format='json')
        
        # Second registration with same email but different phone
        payload2 = self.valid_payload.copy()
        payload2['phone_number'] = '+254798765432'
        payload2['email'] = self.valid_payload['email']  # same email
        
        response = self.client.post(self.register_url, payload2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_register_optional_fields_omitted(self):
        """Test registration works without optional fields (email, farm_name, etc.)"""
        minimal_payload = {
            'phone_number': '+254711223344',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 'consumer',  # consumer doesn't need farm_name
        }
        response = self.client.post(self.register_url, minimal_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(phone_number=minimal_payload['phone_number'])
        self.assertEqual(user.user_type, 'consumer')
        self.assertIsNone(user.farm_name)
    
    def test_login_success(self):
        """Test successful login returns JWT tokens"""
        # First register a user
        self.client.post(self.register_url, self.valid_payload, format='json')
        
        # Then login
        login_payload = {
            'phone_number': self.valid_payload['phone_number'],
            'password': self.valid_payload['password']
        }
        response = self.client.post(reverse('user-login'), login_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['phone_number'], self.valid_payload['phone_number'])

    def test_login_invalid_password(self):
        """Test login with wrong password fails"""
        self.client.post(self.register_url, self.valid_payload, format='json')
        
        login_payload = {
            'phone_number': self.valid_payload['phone_number'],
            'password': 'WrongPass123!'
        }
        response = self.client.post(reverse('user-login'), login_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_login_nonexistent_phone(self):
        """Test login with unregistered phone fails"""
        login_payload = {
            'phone_number': '+254799999999',
            'password': 'AnyPass123!'
        }
        response = self.client.post(reverse('user-login'), login_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)