from django.db.models import fields
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


class orderCreateSer(serializers.Serializer):
    courier = serializers.IntegerField(required=False)
    outlet = serializers.IntegerField()
    products = serializers.ListField()
    type_order = serializers.IntegerField(required=False)
    counterparty = serializers.IntegerField()

class BasketSer(serializers.Serializer):
    products = serializers.ListField()

class BasketGetSer(serializers.ModelSerializer):
    basket_product = OrderProductSer(many=True)
    class Meta:
        model = Basket
        fields = "__all__"

