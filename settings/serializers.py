from rest_framework import serializers
from .models import *

class TypePriceSer(serializers.ModelSerializer):
    class Meta:
        model = Type_Price
        fields = "__all__"


class OrderSectorSer(serializers.ModelSerializer):
    class Meta:
        model = Order_Sector
        fields = "__all__"