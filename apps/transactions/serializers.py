from rest_framework import serializers
from .models import Transaction, TransactionItem

class TransactionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = ('id', 'product', 'product_name', 'quantity', 'unit_price', 'buying_price', 'line_total')

class TransactionSerializer(serializers.ModelSerializer):
    items = TransactionItemSerializer(many=True)

    class Meta:
        model = Transaction
        fields = (
            'id', 'shop', 'branch', 'cashier', 'txn_ref',
            'subtotal', 'vat_amount', 'total', 'discount_amount',
            'payment_method', 'status', 'created_at', 'synced_at', 'local_id', 'items'
        )
        read_only_fields = ('id', 'shop', 'synced_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        transaction = Transaction.objects.create(**validated_data)
        for item_data in items_data:
            TransactionItem.objects.create(transaction=transaction, **item_data)
        return transaction
