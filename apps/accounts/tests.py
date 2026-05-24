from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.shops.models import Shop, Branch

User = get_user_model()

class AccountsTests(APITestCase):
    def test_register_user(self):
        """
        Ensure we can create a new user and a shop simultaneously.
        """
        url = reverse('register')
        data = {
            'email': 'test@shopos.com',
            'full_name': 'Test User',
            'password': 'testpassword123',
            'shop_name': 'Test Shop'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Shop.objects.count(), 1)
        self.assertEqual(Branch.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@shopos.com')

    def test_login_user(self):
        """
        Ensure we can login and get JWT tokens.
        """
        user = User.objects.create_user(email='test@shopos.com', password='testpassword123', full_name='Test User')
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@shopos.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
