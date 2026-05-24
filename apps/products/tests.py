from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.shops.models import Shop, Branch
from apps.products.models import Category, Product

User = get_user_model()

class ProductsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='owner@shop.com', password='password123', full_name='Owner')
        self.shop = Shop.objects.create(owner=self.user, name='Owner Shop')
        self.branch = Branch.objects.create(shop=self.shop, name='Main Branch')
        self.category = Category.objects.create(shop=self.shop, name='Groceries')
        self.client.force_authenticate(user=self.user)

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'branch': self.branch.id,
            'category': self.category.id,
            'name': 'Milk',
            'barcode': '123456',
            'buying_price': 100,
            'selling_price': 120,
            'stock_qty': 10,
            'low_stock_at': 2,
            'local_id': 'local-123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Milk')
