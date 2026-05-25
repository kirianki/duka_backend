from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from .models import JournalEntry, ExpenseCategory, Expense, FinancialAccount
from .serializers import (
    ExpenseCategorySerializer, 
    ExpenseSerializer,
    FinancialAccountSerializer,
    JournalEntrySerializer
)
from apps.core.permissions import IsShopOwner
from apps.shops.models import Shop
from apps.transactions.models import Transaction, TransactionItem

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseCategory.objects.filter(shop=self.request.user.shop)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop)

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(shop=self.request.user.shop)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop)

class FinancialAccountViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FinancialAccount.objects.filter(shop=self.request.user.shop)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop)

class AccountingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def pl_statement(self, request):  # FIX: missing request parameter
        shop = request.user.shop
        
        # Optional date range filters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        txn_qs = Transaction.objects.filter(shop=shop, status=Transaction.Status.COMPLETED)
        exp_qs = Expense.objects.filter(shop=shop)

        if start_date:
            txn_qs = txn_qs.filter(created_at__date__gte=start_date)
            exp_qs = exp_qs.filter(date__gte=start_date)
        if end_date:
            txn_qs = txn_qs.filter(created_at__date__lte=end_date)
            exp_qs = exp_qs.filter(date__lte=end_date)

        # Revenue
        revenue = txn_qs.aggregate(total=Sum('total'))['total'] or 0

        # COGS
        cogs = TransactionItem.objects.filter(
            transaction__in=txn_qs
        ).aggregate(
            total_cogs=Sum(F('buying_price') * F('quantity'))
        )['total_cogs'] or 0
        
        # Expenses
        expenses = exp_qs.aggregate(total=Sum('amount'))['total'] or 0
        
        gross_profit = float(revenue) - float(cogs)
        net_profit = gross_profit - float(expenses)
        
        return Response({
            "revenue": float(revenue),
            "cogs": float(cogs),
            "gross_profit": gross_profit,
            "expenses": float(expenses),
            "net_profit": net_profit
        })

    @action(detail=False, methods=['get'])
    def vat_report(self, request):  # FIX: missing request parameter
        shop = request.user.shop
        vat = Transaction.objects.filter(
            shop=shop, 
            status=Transaction.Status.COMPLETED
        ).aggregate(total=Sum('vat_amount'))['total'] or 0
        
        return Response({"total_vat": float(vat)})
