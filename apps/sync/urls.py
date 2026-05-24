from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SyncViewSet

router = DefaultRouter()
router.register(r'', SyncViewSet, basename='sync')

urlpatterns = [
    path('', include(router.urls)),
]
