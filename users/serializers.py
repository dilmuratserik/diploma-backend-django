from rest_framework import serializers
from .models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.conf import settings


class LoginAdminSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()


class PhoneS(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    # name = serializers.CharField(required=False)

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField()


class AvatarSerializer(serializers.Serializer):
    avatar = serializers.CharField()

class CountrySer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()

from utils.compress import compress_image
class StrogeSer(serializers.Serializer):
    name = serializers.CharField()
class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    # type_price = serializers.IntegerField(read_only_fields)
    storage = StrogeSer()
    class Meta:
        model = User
        fields = ("avatar", "name", 'location', 'bin_iin', 'role', 'phone', 'locations', 'country', 'city', 'type_price', 'storage', 'order_sector')
        # required_fields = ("avatar", "name", 'location', 'bin_iin', 'role', 'phone', 'country', 'city')
        readd_only_fields = ('type_price', 'storage', 'order_sector')

    def update(self, instance, validated_data):
        ava = validated_data.get('avatar', None)
        if ava:
            ava = compress_image(ava, (400, 400))
            instance.avatar = ava
        instance.name = validated_data.get('name', instance.name)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.bin_iin = validated_data.get('bin_iin', instance.bin_iin)
        instance.location = validated_data.get('location', instance.location)
        instance.role = validated_data.get('role', instance.role)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

    def create(self, validated_data):
        pass


class pushSerializer(serializers.Serializer):
	reg_id = serializers.CharField()
	cmt = serializers.CharField()


class Registration(serializers.Serializer):
    password = serializers.CharField()
    bin_iin = serializers.CharField(required=False)
    name  = serializers.CharField()
    country = serializers.IntegerField()
    city = serializers.IntegerField()
    role = serializers.IntegerField()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    


class TPUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("avatar", "name", 'type_price', 'storage', 'order_sector', 'phone', 'id')
        read_only_fields = ('id',)
        # required_fields = ("avatar", "name", 'location', 'bin_iin', 'role')

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.name = validated_data.get('name', instance.name)
        instance.order_sector = validated_data.get('order_sector', instance.order_sector)
        instance.type_price = validated_data.get('type_price', instance.type_price)
        instance.storage = validated_data.get('storage', instance.storage)
        instance.save()
        return instance


class CourierUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("avatar", "name", 'type_price', 'storage', 'order_sector', 'phone', 'id')
        read_only_fields = ('id',)
        # required_fields = ("avatar", "name", 'location', 'bin_iin', 'role')

    def update(self, instance, validated_data):
        print(validated_data.get('avatar'), 'None')
        if validated_data.get('avatar'):
            instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.name = validated_data.get('name', instance.name)
        instance.order_sector = validated_data.get('order_sector', instance.order_sector)
        instance.type_price = validated_data.get('type_price', instance.type_price)
        instance.storage = validated_data.get('storage', instance.storage)
        instance.save()
        return instance


class contgentSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'role', 'bin_iin', 'phone')