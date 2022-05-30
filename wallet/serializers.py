from rest_framework import serializers
from django.contrib.auth.models import User 
from wallet.models import UserWallet , Payment


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    payment_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Payment
        fields = '__all__'
        # depth = 2 # Using depth option on serializers should not ignore foreign keys on post/create actions 