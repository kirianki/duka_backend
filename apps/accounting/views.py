from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from .models import JournalEntry, ExpenseCategory, Expense
from .serializers import JournalEntrySerializer, ExpenseCategorySerializer, ExpenseSerializer
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

class AccountingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def pl_statement(self):
        shop = self.request.user.shop
        
        # Revenue
        revenue = Transaction.objects.filter(
            shop=shop, 
            status=Transaction.Status.COMPLETED
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # COGS
        cogs = TransactionItem.objects.filter(
            transaction__shop=shop,
            transaction__status=Transaction.Status.COMPLETED
        ).aggregate(
            total_cogs=Sum(F('buying_price') * F('quantity'))
        )['total_cogs'] or 0
        
        # Expenses
        expenses = Expense.objects.filter(shop=shop).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
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
    def vat_report(self):
        shop = self.request.user.shop
        vat = Transaction.objects.filter(
            shop=shop, 
            status=Transaction.Status.COMPLETED
        ).aggregate(total=Sum('vat_amount'))['total'] or 0
        
        return Response({"total_vat": float(vat)})
