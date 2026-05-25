from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Shopkeeper

User = get_user_model()

class OwnerSerializer(serializers.ModelSerializer):
    shop_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'date_joined', 'shop_name')
        read_only_fields = ('id', 'date_joined')

    def get_shop_name(self, obj):
        shop = getattr(obj, 'shop', None)
        return shop.name if shop else None

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    shop_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'shop_name')

    def create(self, validated_data):
        shop_name = validated_data.pop('shop_name')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name']
        )
        # Shop creation will be handled in the view or via signal
        return user

class ShopkeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopkeeper
        fields = ('id', 'owner', 'branch', 'full_name', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at', 'owner')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = OwnerSerializer(self.user).data
        return data
