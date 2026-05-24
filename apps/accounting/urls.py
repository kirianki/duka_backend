from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountingViewSet

router = DefaultRouter()
router.register(r'', AccountingViewSet, basename='accounting')

urlpatterns = [
    path('', include(router.urls)),
]
