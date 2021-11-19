from django.shortcuts import render
from rest_framework.views import APIView
import random
from .serializers import *
from .models import User, PhoneOTP
from locations.models import Country, City
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from django.contrib.auth import (login as django_login,
                                 logout as django_logout)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveUpdateAPIView
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)
from django.utils.translation import ugettext_lazy as _
from rest_framework import status

# from products.models import *
# from utils.compress import *
# from push_notifications.models import APNSDevice, GCMDevice
# from utils.push import send_push
# from utils.smsc_api import SMSC
# smsc = SMSC()



class PhoneCode(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = PhoneS(data=request.data)
        rand = random.randint(1000, 9999)
        if s.is_valid():
            phone = s.validated_data['phone']
            user = User.objects.filter(phone=phone)
            if user.exists():
                return Response({'status': 'already exists'})
            else:
                p = PhoneOTP.objects.filter(phone = phone)
                if p.exists():
                    a = p.first()
                    if phone == "77783579279":
                        a.otp = "1111"
                    else:
                        a.otp = rand
                    a.save()
                else:
                    if phone == "77783579279":
                        PhoneOTP.objects.create(phone=phone, otp="1111")
                    else:
                        PhoneOTP.objects.create(phone=phone, otp=str(rand))
                # if phone != "+77783579279":
                    # smsc.send_sms(phone, "Код подтверждения для ALU.KZ: "+str(rand), sender="sms")
                return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class Register(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            print('register: ', s.validated_data['phone'], s.validated_data['code'])
            phone = s.validated_data['phone']
            u = PhoneOTP.objects.get(phone=phone)
            if u.otp == str(s.validated_data['code']):
                # u.validated = True
                # nickname = u.nickname
                # u.save()
                if User.objects.filter(phone=phone).exists():
                    us = User.objects.get(phone=phone)
                    uid = us.pk
                    # us.nickname = nickname
                    us.save()
                else:
                    us = User.objects.create(phone=phone)
                    uid = us.pk
                if Token.objects.filter(user=us).exists():
                    token = Token.objects.get(user=us)
                else:
                    token = Token.objects.create(user=us)
                # user = authenticate(phone=phone)
                # django_login(request, us)
                return Response({'key': token.key, 'uid': uid, 'status': 'ok'})
            else:
                return Response({'status': 'otp error'})
        else:
            return Response(s.errors)


class RegisterationContinue(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        s = Registration(data=request.data)
        if s.is_valid():
            user = request.user
            role = s.validated_data['role']
            if role == 1:
                user.role = 1
                user.name = s.validated_data['name']
                user.country = Country.objects.get(id=s.validated_data['country'])
                user.city = City.objects.get(id=s.validated_data['city'])
            elif role == 2:
                user.role = 2
                user.name = s.validated_data['name']
                user.country = Country.objects.get(id=s.validated_data['country'])
                user.city = City.objects.get(id=s.validated_data['city'])
                user.bin_iin = s.validated_data['bin_iin']
            user.set_password(s.validated_data['password'])
            user.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)
        


class Logined(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = LoginAdminSerializer(data=request.data)
        if s.is_valid():
            phone = s.validated_data['phone']
            pwd = s.validated_data['password']
            try:
                us = User.objects.get(phone=phone)
            except ValueError:
                us = None
            if us:
                if us.check_password(pwd):
                    if Token.objects.filter(user=us).exists():
                        token = Token.objects.get(user=us)
                    else:
                        token = Token.objects.create(user=us)
                    return Response({'key': token.key, 'uid': us.id, 'status': 'ok', 'role': us.role})
                else:
                    return Response({'status': 'error'})
            else:
                return Response({'status': 'not found'})
        else:
            return Response(s.errors)


from utils.compress import compress_image
class Avatar(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = AvatarSerializer(data=request.data)
        if s.is_valid():
            ava = s.validated_data['avatar']
            ava = compress_image(ava, (400, 400))
            request.user.avatar = ava
            request.user.save()
            return Response({'status': "ok", "avatar": request.user.avatar.url})
        else:
            return Response(s.errors)


class detailUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        u = User.objects.values("id", "avatar", "name", "phone", "role").get(id = id)
        return Response(u)


class detailUser2(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PasswordChangeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = PasswordChangeSerializer(data=request.data)
        if s.is_valid():
            user = request.user
            if user.check_password(s.validated_data['old_password']):
                user.set_password(s.validated_data['new_password'])
                user.save()
                return Response({'status': 'ok'})
            else:
                return Response({'status': 'error'})
        else:
            return Response({'status': 'error'})
    


class login_admin(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = LoginAdminSerializer(data=request.data)
        if s.is_valid():
            phone = s.validated_data['phone']
            password = s.validated_data['password']
            if User.objects.filter(phone=phone, is_staff=True).exists():
                us = User.objects.get(phone=phone)
                if us.check_password(password):
                    us = us
                else:
                    return Response({'status': 'error'})
            else:
                return Response({'status': 'error'})
            if Token.objects.filter(user=us).exists():
                token = Token.objects.get(user=us)
            else:
                token = Token.objects.create(user=us)
            # django_login(request, us)
            return Response({'key': token.key, 'uid': us.pk})
        else:
            return Response(s.errors)



class TPUserView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.filter(role__in=(3, 4))
    serializer_class = TPUserSerializer

    def create(self, request):
        s = CourierUserSerializer(data=request.data)
        if s.is_valid():
            user = User.objects.create(**s.validated_data)
            user.set_password(s.validated_data['password'])
            user.save()
            ser = TPUserSerializer(user)
            return Response(ser.data)
        else:
            return Response(s.errors, status=status.HTTP_409_CONFLICT)
    
    def update(self, request, pk=None):
        s = CourierUserSerializer(data=request.data)
        if s.is_valid():
            instance = User.objects.get(id=pk)
            validated_data = s.validated_data
            instance.role = validated_data.get('role', instance.role)
            ava = validated_data.get('avatar', None)
            if ava:
                ava = compress_image(ava, (400, 400))
                instance.avatar = ava
            instance.name = validated_data.get('name', instance.name)
            instance.show_plan = validated_data.get('show_plan', instance.show_plan)
            instance.order_sector = validated_data.get('order_sector', instance.order_sector)
            instance.type_price = validated_data.get('type_price', instance.type_price)
            instance.storage = validated_data.get('storage', instance.storage)
            pwd = s.validated_data.get('password', None)
            if pwd:
                instance.set_password = pwd
            instance.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class GetPointListApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = User.objects.filter(role=2)
        s = CountrySer(queryset, many=True)
        return Response(s.data)



class GetPointDetailApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = User.objects.filter(role=2)
        s = PointSer(queryset, many=True)
        return Response(s.data)

    def post(self, request):
        s = PointSer(data=request.data)
        if s.is_valid():
            p = User.objects.create(
                phone = s.validated_data['phone'],
                name = s.validated_data['name'],
                bin_iin = s.validated_data['bin_iin'],
                order_sector = s.validated_data['order_sector']
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


# class pushRegister(APIView):
#     permission_classes = [permissions.IsAuthenticated]
    
#     def post(self, request):
#         s = pushSerializer(data=request.data)
#         if s.is_valid():
#             cmt = s.validated_data['cmt']
#             if cmt == "apn":
#                 ios = APNSDevice.objects.filter(user = request.user)
#                 if ios.exists():
#                     ios = APNSDevice.objects.get(user = request.user)
#                     ios.registration_id = s.validated_data['reg_id']
#                     ios.save()
#                 else:
#                     APNSDevice.objects.create(user=request.user, registration_id=s.validated_data['reg_id'])
#             else:
#                 android = GCMDevice.objects.filter(user=request.user)
#                 if android.exists():
#                     android = GCMDevice.objects.get(user=request.user)
#                     android.registration_id = s.validated_data['reg_id']
#                     android.save()
#                 else:
#                     GCMDevice.objects.create(user=request.user, active=True,
#                                         registration_id=s.validated_data['reg_id'],
#                                         cloud_message_type="FCM")
#             return Response({'status': "ok"})
#         else:
#             return Response(s.errors)


# def privatepolicy(request):
#     context = {'context': ""}
#     return render(request, 'index.html', context)

