from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountingViewSet, ExpenseCategoryViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'expenses/categories', ExpenseCategoryViewSet, basename='expense-categories')
router.register(r'expenses', ExpenseViewSet, basename='expenses')
router.register(r'', AccountingViewSet, basename='accounting')

urlpatterns = [
    path('', include(router.urls)),
]
