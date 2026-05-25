from django.db import models
from apps.shops.models import Shop, Branch
from apps.transactions.models import Transaction

class JournalEntry(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='journal_entries')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='journal_entries')
    entry_ref = models.CharField(max_length=50, unique=True)
    entry_type = models.CharField(max_length=30)  # sale|expense|adjustment
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, related_name='journal_entries')
    posted_at = models.DateTimeField()
    posted_by = models.CharField(max_length=100)
    local_id = models.CharField(max_length=64, db_index=True)

    class Meta:
        verbose_name_plural = "Journal Entries"

    def __str__(self):
        return self.entry_ref

class FinancialAccount(models.Model):
    ACCOUNT_TYPES = (
        ('CASH', 'Cash'),
        ('MPESA', 'M-Pesa Float'),
        ('BANK', 'Bank'),
        ('OTHER', 'Other'),
    )
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='financial_accounts')
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.balance})"

class JournalLine(models.Model):
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(FinancialAccount, on_delete=models.SET_NULL, null=True, related_name='journal_lines')
    account_name = models.CharField(max_length=100) # Fallback / descriptive
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account_name} ({'DR' if self.debit > 0 else 'CR'})"

class ExpenseCategory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='expense_categories')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Expense Categories"

    def __str__(self):
        return f"{self.shop.name} - {self.name}"

class Expense(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='expenses')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='expenses')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, related_name='expenses')
    account = models.ForeignKey(FinancialAccount, on_delete=models.SET_NULL, null=True, related_name='expenses')
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    local_id = models.CharField(max_length=64, db_index=True)

    def __str__(self):
        return f"{self.description} ({self.amount})"
