from rest_framework import serializers
from .models import MpesaConfig

class MpesaConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaConfig
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        payment_type = data.get('payment_type')
        if payment_type == MpesaConfig.PaymentType.PAYBILL and not data.get('account_number'):
            raise serializers.ValidationError({"account_number": "Account number is required for Paybill."})
        if payment_type == MpesaConfig.PaymentType.POCHI and not data.get('phone_number'):
            raise serializers.ValidationError({"phone_number": "Phone number is required for Pochi la Biashara."})
        return data
