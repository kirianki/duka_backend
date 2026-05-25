from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        transaction = self.get_object()
        if transaction.status == Transaction.Status.PENDING:
            transaction.status = Transaction.Status.COMPLETED
            transaction.save()
            return Response({'status': 'confirmed'})
        return Response({'error': 'Transaction is not pending'}, status=400)
