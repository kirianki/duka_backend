from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, BranchViewSet

router = DefaultRouter()
router.register(r'profile', ShopViewSet, basename='shop')
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]
