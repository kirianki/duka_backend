from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.shops.models import Shop, Branch
from apps.products.models import Product, Category
from .models import Transaction

User = get_user_model()

class TransactionsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='owner@shop.com', password='password123', full_name='Owner')
        self.shop = Shop.objects.create(owner=self.user, name='Owner Shop')
        self.branch = Branch.objects.create(shop=self.shop, name='Main Branch')
        self.category = Category.objects.create(shop=self.shop, name='Groceries')
        self.product = Product.objects.create(
            shop=self.shop, branch=self.branch, category=self.category,
            name='Soap', buying_price=50, selling_price=70, stock_qty=100
        )
        self.client.force_authenticate(user=self.user)

    def test_create_transaction_with_items(self):
        url = reverse('transaction-list')
        data = {
            'branch': self.branch.id,
            'txn_ref': 'TXN-123',
            'subtotal': 140,
            'vat_amount': 22.4,
            'total': 162.4,
            'payment_method': 'CASH',
            'status': 'COMPLETED',
            'local_id': 'local-txn-123',
            'created_at': '2026-05-24T12:00:00Z',
            'items': [
                {
                    'product': self.product.id,
                    'product_name': 'Soap',
                    'quantity': 2,
                    'unit_price': 70,
                    'buying_price': 50,
                    'line_total': 140
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().items.count(), 1)
