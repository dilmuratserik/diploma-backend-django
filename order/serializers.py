from rest_framework import serializers
from .models import *
from users.serializers import contgentSer
from product.serializers import productSer2


class productser(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    articul = serializers.CharField()

class OrderSer(serializers.ModelSerializer):
    products = productser(many=True)
    counterparty = contgentSer()
    class Meta:
        model = Order
        fields = ('date', 'products', 'counterparty', 'status', 'outlet', 'type_order', 'products_count')