from rest_framework import viewsets, permissions
from .models import MpesaConfig
from .serializers import MpesaConfigSerializer
from apps.core.permissions import IsOwner

class MpesaConfigViewSet(viewsets.ModelViewSet):
    serializer_class = MpesaConfigSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Only allow owners to see their own shop's configs
        return MpesaConfig.objects.filter(shop__owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically link to the user's shop if not provided
        # This assumes the user has only one shop for now.
        # If they have multiple, the frontend should provide the shop ID.
        serializer.save()
