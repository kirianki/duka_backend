from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

class SyncViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def push_data(self, request):
        return Response({"status": "success", "synced_count": 0}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def pull_data(self, request):
        return Response({"data": []}, status=status.HTTP_200_OK)
