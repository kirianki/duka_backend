from rest_framework import serializers
from .models import JournalEntry, ExpenseCategory, Expense

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ('id', 'shop', 'name')
        read_only_fields = ('id', 'shop')

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Expense
        fields = (
            'id', 'shop', 'branch', 'category', 'category_name',
            'description', 'amount', 'date', 'created_at', 'local_id'
        )
        read_only_fields = ('id', 'shop', 'created_at')
