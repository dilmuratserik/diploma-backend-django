from rest_framework import serializers
from .models import *

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("city", "address")



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class AddressSer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ('user',)

class IdSer(serializers.Serializer):
    id = serializers.IntegerField()



class StorageSer(serializers.ModelSerializer):
    class Meta:
        model = Storage_region
        fields = "__all__"