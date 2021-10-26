from rest_framework import serializers
from .models import *

class ProductImageSer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_avatar_url')
    class Meta:
        model = ProductImage
        fields = ("image",)
    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

class productSer(serializers.ModelSerializer):
    product_image = ProductImageSer(many=True)
    class Meta:
        model = Product
        fields = "__all__"


class ProductGetSer(serializers.Serializer):
    name = serializers.CharField(required=False)
    unit = serializers.IntegerField(required=False)
    price = serializers.IntegerField(required=False)
    articul = serializers.CharField(required=False)


class getProductSer(serializers.Serializer):
    data = serializers.ListField()
