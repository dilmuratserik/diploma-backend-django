from django.db.models import fields
from rest_framework import serializers
from .models import *
from users.serializers import contgentSer
from product.serializers import productSer2


class productser(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    articul = serializers.CharField()
    price = serializers.IntegerField()

class OrderProductSer(serializers.ModelSerializer):
    product = productser()
    class Meta:
        model = OrderProduct
        fields = "__all__"

class OrderSer(serializers.ModelSerializer):
    product_order = OrderProductSer(many=True)
    counterparty = contgentSer()
    # sum = serializers.IntegerField()
    class Meta:
        model = Order
        fields = "__all__"


class orderCreateSer(serializers.Serializer):
    courier = serializers.IntegerField(required=False)
    products = serializers.ListField()
    type_order = serializers.IntegerField(required=False)
    counterparty = serializers.IntegerField()
    type_delivery = serializers.IntegerField(required=False)
    delivered_date = serializers.DateField(required=False)
    delivery_address = serializers.IntegerField(required=False)
    pickup_address = serializers.IntegerField(required=False)
    bonus = serializers.BooleanField(required=False)



class ScheduleSer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"

class PointSer(serializers.Serializer):
    name = serializers.CharField()
class ScheduleGetSer(serializers.ModelSerializer):
    point = PointSer()
    class Meta:
        model = Schedule
        fields = "__all__"


class ScheduleChangeSer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    plan = serializers.BooleanField()
    fact = serializers.BooleanField()
    comments = serializers.CharField()


class CourierOrderSer(serializers.Serializer):
    id=serializers.IntegerField()
    comment = serializers.CharField(required=False)
    status = serializers.IntegerField(required=False)
    date = serializers.DateField(required=False)


class AddCourierToOrderSer(serializers.Serializer):
    order_id = serializers.IntegerField()
    courier_id = serializers.IntegerField()

# class BasketSer(serializers.Serializer):
#     products = serializers.ListField()

# class BasketGetSer(serializers.ModelSerializer):
#     basket_product = OrderProductSer(many=True)
#     class Meta:
#         model = Basket
#         fields = "__all__"

