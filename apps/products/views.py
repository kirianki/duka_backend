from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from apps.core.permissions import IsShopOwner
from apps.shops.models import Shop

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsShopOwner]

    def get_queryset(self):
        return Category.objects.filter(shop__owner=self.request.user)

    def perform_create(self, serializer):
        shop = Shop.objects.get(owner=self.request.user)
        serializer.save(shop=shop)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['branch', 'category', 'is_active']
    search_fields = ['name', 'barcode']

    def get_queryset(self):
        return Product.objects.filter(shop__owner=self.request.user)

    def perform_create(self, serializer):
        shop = Shop.objects.get(owner=self.request.user)
        serializer.save(shop=shop)
