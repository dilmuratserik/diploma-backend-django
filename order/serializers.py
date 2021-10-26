from rest_framework import serializers
from .models import *


class ProductSer(serializers.Serializer):
    code = serializers.CharField()

class OrderSer(serializers.ModelSerializer):
    products = ProductSer(many=True)
    class Meta:
        model = Order
        fields = "__all__"