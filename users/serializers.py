from rest_framework import serializers
from .models import User
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


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    # type_price = serializers.IntegerField(read_only_fields)
    storage = CountrySer(read_only=True)
    price_type = CountrySer(read_only=True)
    sector_order = CountrySer(read_only=True)
    class Meta:
        model = User
        fields = ("avatar", "name", 'location', 'bin_iin', 'role', 'phone', 'locations', 'country', 'city', 'price_type', 'storage', 'sector_order', 'working_hour_until', 'working_hour_with')
        # required_fields = ("avatar", "name", 'location', 'bin_iin', 'role', 'phone', 'country', 'city')
        read_only_fields = ('working_hour_until', 'storage', 'working_hour_with')

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
    storage = CountrySer()
    price_type = CountrySer()
    sector_order = CountrySer()
    class Meta:
        model = User
        fields = ("avatar", "name", 'price_type','type_price', 'storage', 'sector_order', 'order_sector', 'phone', 'id',  'role', 'show_plan', 'working_hour_with', 'working_hour_until')
        read_only_fields = ('id',)

class CourierUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ("avatar", "name", 'price_type', 'type_price', 'storage', 'sector_order', 'order_sector', 'phone', 'id', 'role', 'password', 'show_plan', 'agent', 'working_hour_with', 'working_hour_until')
        read_only_fields = ('id',)

class contgentSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name', 'role', 'bin_iin', 'phone')


class PointSer(serializers.ModelSerializer):
    agent = CountrySer()
    storage = CountrySer()
    city = CountrySer()
    class Meta:
        model = User
        fields = ("id", "phone", "name", "bin_iin", "credit", "paymets", "debt", "order_sector", 'agent', 'storage', 'city')
        read_only_fields = ("id",)

class CreatePointSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone", "name", "bin_iin", "sector_order", 'storage', 'city')


class AddAgenttoPointSer(serializers.Serializer):
    agent = serializers.IntegerField()
