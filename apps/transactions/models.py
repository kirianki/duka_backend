from django.db import models
from apps.shops.models import Shop, Branch
from apps.accounts.models import Shopkeeper
from apps.products.models import Product

class Transaction(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Cash'
        MPESA = 'MPESA', 'M-Pesa'
        QR = 'QR', 'QR Code'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        REFUNDED = 'REFUNDED', 'Refunded'

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='transactions')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='transactions')
    cashier = models.ForeignKey(Shopkeeper, on_delete=models.SET_NULL, null=True, related_name='transactions')
    txn_ref = models.CharField(max_length=50, unique=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField()  # device timestamp
    synced_at = models.DateTimeField(auto_now_add=True)
    local_id = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return self.txn_ref

class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)  # snapshot at time of sale
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
