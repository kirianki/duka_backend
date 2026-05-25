from rest_framework import serializers
from apps.shops.models import Shop, Branch
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'shop', 'name', 'sort_order')
        read_only_fields = ('id', 'shop')

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = (
            'id', 'shop', 'branch', 'category', 'category_name',
            'name', 'barcode', 'buying_price', 'selling_price',
            'stock_qty', 'low_stock_at', 'is_active', 'updated_at', 
            'local_id', 'image', 'unit', 'description'
        )
        read_only_fields = ('id', 'shop', 'updated_at')
