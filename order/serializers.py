from rest_framework import serializers
from .models import *
from users.serializers import contgentSer
class ProductSer(serializers.Serializer):
    code = serializers.CharField()

class OrderSer(serializers.ModelSerializer):
    products = ProductSer(many=True)
    counterparty = contgentSer()
    class Meta:
        model = Order
        fields = "__all__"