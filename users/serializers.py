from rest_framework import serializers
from .models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.conf import settings
from utils.compress import compress_image

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
    avatar = serializers.FileField()

class CountrySer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()

class StrogeSer(serializers.Serializer):
    name = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    # type_price = serializers.IntegerField(read_only_fields)
    storage = StrogeSer(read_only=True)
    class Meta:
        model = User
        fields = ("avatar", "name", 'location', 'bin_iin', 'role', 'phone', 'locations', 'country', 'city', 'type_price', 'storage', 'order_sector')
        # required_fields = ("avatar", "name", 'location', 'bin_iin', 'role', 'phone', 'country', 'city')
        read_only_fields = ('type_price', 'storage', 'order_sector')

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
    storage = StrogeSer()
    class Meta:
        model = User
        fields = ("avatar", "name", 'type_price', 'storage', 'order_sector', 'phone', 'id', 'password', 'role', 'show_plan')
        read_only_fields = ('id',)

class CourierUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ("avatar", "name", 'type_price', 'storage', 'order_sector', 'phone', 'id', 'role', 'password', 'show_plan', 'agent')
        read_only_fields = ('id',)

class contgentSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name', 'role', 'bin_iin', 'phone')


class PointSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone", "name", "bin_iin", "credit", "paymets", "debt", "order_sector", 'agent')
        read_only_fields = ("id",)


class AddAgenttoPointSer(serializers.Serializer):
    agent = serializers.IntegerField()
