from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.transactions.models import Transaction, TransactionItem
from .models import JournalEntry, JournalLine, Expense, FinancialAccount
from django.utils import timezone
import uuid

@receiver(post_save, sender=Transaction)
def handle_transaction_completion(sender, instance, created, **kwargs):
    """
    Handle journal entry creation and stock deduction when a transaction is COMPLETED.
    Works for both new COMPLETED transactions and PENDING -> COMPLETED transitions.
    """
    # We only act if the status is COMPLETED
    if instance.status != Transaction.Status.COMPLETED:
        return

    # Check if we've already processed this transaction (idempotency)
    if JournalEntry.objects.filter(transaction=instance).exists():
        return

    # 1. Determine accounts
    shop = instance.shop
    payment_method = instance.payment_method
    
    # Get or create payment account
    account_type = 'CASH' if payment_method == 'CASH' else 'MPESA'
    account_name = 'Cash Box' if payment_method == 'CASH' else 'M-Pesa Float'
    
    account, _ = FinancialAccount.objects.get_or_create(
        shop=shop,
        account_type=account_type,
        defaults={'name': account_name, 'is_default': True}
    )

    # 2. Create Journal Entry
    entry = JournalEntry.objects.create(
        shop=shop,
        branch=instance.branch,
        entry_ref=f"SALE-{instance.txn_ref}",
        entry_type='sale',
        transaction=instance,
        posted_at=timezone.now(),
        posted_by='system',
        local_id=str(uuid.uuid4())
    )

    # 3. Create Journal Lines (Double Entry)
    # Debit: Asset (Cash/M-Pesa)
    JournalLine.objects.create(
        entry=entry,
        account=account,
        account_name=account.name,
        debit=instance.total,
        credit=0
    )
    
    # Credit: Revenue (Sales)
    JournalLine.objects.create(
        entry=entry,
        account=None,
        account_name="Sales Revenue",
        debit=0,
        credit=instance.total
    )

    # Update account balance
    account.balance += instance.total
    account.save()

    # 4. Deduct Stock
    for item in instance.items.all():
        if item.product:
            from apps.products.models import Product
            Product.objects.filter(pk=item.product.pk).update(
                stock_qty=models.F('stock_qty') - item.quantity
            )

@receiver(post_save, sender=Expense)
def create_expense_journal_entry(sender, instance, created, **kwargs):
    if created:
        shop = instance.shop
        
        # Use explicitly linked account if provided, else fall back to default
        account = getattr(instance, 'account', None)
        if not account:
            account = FinancialAccount.objects.filter(shop=shop, is_default=True).first()
        
        if not account:
            account, _ = FinancialAccount.objects.get_or_create(
                shop=shop,
                account_type='CASH',
                defaults={'name': 'Cash Box', 'is_default': True}
            )

        entry = JournalEntry.objects.create(
            shop=shop,
            branch=instance.branch,
            entry_ref=f"EXP-{instance.id}",
            entry_type='expense',
            posted_at=timezone.now(),
            posted_by='system',
            local_id=instance.local_id or str(uuid.uuid4())
        )

        # Debit: Expense
        JournalLine.objects.create(
            entry=entry,
            account=None,
            account_name=f"Expense: {instance.category.name if instance.category else 'General'}",
            debit=instance.amount,
            credit=0
        )

        # Credit: Asset (Cash/M-Pesa)
        JournalLine.objects.create(
            entry=entry,
            account=account,
            account_name=account.name,
            debit=0,
            credit=instance.amount
        )
        
        # Update balance
        account.balance -= instance.amount
        account.save()
