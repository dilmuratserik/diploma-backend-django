from rest_framework import serializers
from .models import *
from users.serializers import contgentSer
from product.serializers import productSer2

class OrderSer(serializers.ModelSerializer):
    products = productSer2(many=True)
    counterparty = contgentSer()
    class Meta:
        model = Order
        fields = "__all__"