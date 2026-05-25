from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountingViewSet, ExpenseCategoryViewSet, ExpenseViewSet, FinancialAccountViewSet

router = DefaultRouter()
router.register(r'expenses/categories', ExpenseCategoryViewSet, basename='expense-categories')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'accounts', FinancialAccountViewSet, basename='account')
router.register(r'', AccountingViewSet, basename='accounting')

urlpatterns = [
    path('', include(router.urls)),
]
