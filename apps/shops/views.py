from rest_framework import viewsets, permissions
from .models import Shop, Branch
from .serializers import ShopSerializer, BranchSerializer
from apps.core.permissions import IsShopOwner

class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopOwner]

    def get_queryset(self):
        return Shop.objects.filter(owner=self.request.user)

class BranchViewSet(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopOwner]

    def get_queryset(self):
        return Branch.objects.filter(shop__owner=self.request.user)

    def perform_create(self, serializer):
        shop = Shop.objects.get(owner=self.request.user)
        serializer.save(shop=shop)
