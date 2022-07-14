from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import Item , Cart



class ItemSerializer(serializers.ModelSerializer):
    # https://stackoverflow.com/a/66192049/13056176 (say why we should not have readonly here)
    class Meta:
        model = Item
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Cart
        fields = '__all__'
        depth = 2
   