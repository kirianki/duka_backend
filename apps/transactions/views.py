from rest_framework import viewsets, permissions
from .models import Transaction
from .serializers import TransactionSerializer
from apps.core.permissions import IsShopOwner
from apps.shops.models import Shop

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopOwner]

    def get_queryset(self):
        return Transaction.objects.filter(shop__owner=self.request.user)

    def perform_create(self, serializer):
        shop = Shop.objects.get(owner=self.request.user)
        serializer.save(shop=shop)
