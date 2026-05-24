from rest_framework import serializers
from .models import Shop, Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'shop', 'name', 'address', 'mpesa_till', 'mpesa_paybill', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at', 'shop')

class ShopSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = ('id', 'owner', 'name', 'kra_pin', 'logo_url', 'vat_rate', 'vat_inclusive', 'branches', 'created_at')
        read_only_fields = ('id', 'created_at', 'owner')
