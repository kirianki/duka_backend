from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.shops.models import Shop, Branch
from .serializers import OwnerSerializer, RegisterSerializer, ShopkeeperSerializer
from .models import Shopkeeper

User = get_user_model()

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create Shop and initial Branch automatically
        shop = Shop.objects.create(
            owner=user,
            name=request.data.get('shop_name', f"{user.full_name}'s Shop")
        )
        Branch.objects.create(
            shop=shop,
            name="Main Branch"
        )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "user": OwnerSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": "User registered successfully with shop and main branch."
        }, status=status.HTTP_201_CREATED)

class OwnerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = OwnerSerializer
    
    def get_object(self):
        return self.request.user

class ShopkeeperViewSet(generics.ListCreateAPIView):
    serializer_class = ShopkeeperSerializer

    def get_queryset(self):
        return Shopkeeper.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
