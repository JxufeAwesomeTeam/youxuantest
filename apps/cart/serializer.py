from rest_framework import serializers
from .models import CartItem

from apps.login.serializer import  UserSerializer
class CartItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'
        depth =2