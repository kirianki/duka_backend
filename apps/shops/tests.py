from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Shop, Branch

User = get_user_model()

class ShopsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='owner@shop.com', password='password123', full_name='Owner')
        self.shop = Shop.objects.create(owner=self.user, name='Owner Shop')
        self.client.force_authenticate(user=self.user)

    def test_list_branches(self):
        Branch.objects.create(shop=self.shop, name='Branch 1')
        url = reverse('branch-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_branch(self):
        url = reverse('branch-list')
        data = {'name': 'New Branch', 'address': '123 St'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Branch.objects.count(), 1)
