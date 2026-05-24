from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.shops.models import Shop, Branch
from .models import MpesaConfig

User = get_user_model()

class PaymentsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='owner@shop.com', password='password123', full_name='Owner')
        self.shop = Shop.objects.create(owner=self.user, name='Owner Shop')
        self.client.force_authenticate(user=self.user)

    def test_create_mpesa_config_paybill(self):
        url = reverse('mpesaconfig-list')
        data = {
            'shop': self.shop.id,
            'payment_type': 'PAYBILL',
            'business_number': '123456',
            'account_number': 'ACC-123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MpesaConfig.objects.count(), 1)

    def test_create_mpesa_config_invalid_paybill(self):
        # Missing account number for Paybill
        url = reverse('mpesaconfig-list')
        data = {
            'shop': self.shop.id,
            'payment_type': 'PAYBILL',
            'business_number': '123456'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('account_number', response.data)
