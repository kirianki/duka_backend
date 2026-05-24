from django.db import models
from apps.transactions.models import Transaction
from apps.shops.models import Shop, Branch

class MpesaConfig(models.Model):
    class PaymentType(models.TextChoices):
        PAYBILL = 'PAYBILL', 'Paybill'
        TILL = 'TILL', 'Buy Goods (Till)'
        POCHI = 'POCHI', 'Pochi la Biashara'

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='mpesa_configs')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='mpesa_configs', null=True, blank=True)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices)
    business_number = models.CharField(max_length=20, help_text="Paybill or Till Number")
    account_number = models.CharField(max_length=50, blank=True, help_text="Required for Paybill")
    phone_number = models.CharField(max_length=15, blank=True, help_text="Required for Pochi")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shop.name} - {self.payment_type}"

class MpesaTransaction(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='mpesa_details')
    phone_number = models.CharField(max_length=15)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    merchant_request_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='PENDING')
    mpesa_receipt = models.CharField(max_length=50, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    failure_reason = models.TextField(blank=True)
    initiated_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.transaction.txn_ref} - {self.phone_number}"
