from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JournalEntry
from .serializers import JournalEntrySerializer

class AccountingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def pl_statement(self, request):
        return Response({"message": "P&L Statement placeholder"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def vat_report(self, request):
        return Response({"message": "VAT Report placeholder"}, status=status.HTTP_200_OK)
