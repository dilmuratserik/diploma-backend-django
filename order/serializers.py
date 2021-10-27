from rest_framework import serializers
from .models import *
from users.serializers import contgentSer
from product.serializers import productSer2


class productser(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    articul = serializers.CharField()

class OrderProductSer(serializers.ModelSerializer):
    product = productser()
    class Meta:
        model = OrderProduct
        fields = "__all__"

class OrderSer(serializers.ModelSerializer):
    product_order = OrderProductSer(many=True)
    counterparty = contgentSer()
    class Meta:
        model = Order
        fields = "__all__"