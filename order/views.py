import re
from django.db.models import manager
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.views import APIView
import random
from product.models import Product
from .serializers import *
from .models import *
from locations.models import Country, City, Outlets
from users.models import User
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveUpdateAPIView
from datetime import date, datetime
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination 


class OrderApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        o = Order.objects.all()
        s = OrderSer(o, many=True)
        return Response(s.data)


class CreateOrderApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Order.objects.filter(status = 1)
        ser = OrderSer(queryset, many=True)
        return Response(ser.data)

    def post(self, request):
        s = orderCreateSer(data=request.data)
        if s.is_valid():
            print(s.validated_data)
            order = Order.objects.create(
                type_delivery = s.validated_data.get('type_delivery', 1),
                # outlet = Outlets.objects.get(s.validated_data['outlet']),
                counterparty = User.objects.get(['counterparty']),
                delivered_date = s.validated_data.get('delivered_date', None)
            )
            products = s.validated_data['products']
            for i in products:
                p = Product.objects.get(id=i['id'])
                OrderProduct.objects.create(
                    product = p,
                    count = i['count'],
                    order = order
                )
                p.count_order += 1
                p.save()
            return Response({'status': "ok"})
        else:
            return Response(s.errors)


class CourierOrderHistory(APIView):
    permission_classes = (permissions.IsAuthenticated,)\

    def get(self, request):
        queryset = Order.objects.filter(status__in=(3,4), courier = request.user)
        s = OrderSer(queryset, many=True)
        return Response(s.data)


class ScheduleApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Schedule.objects.filter(agent = request.user)
        s = ScheduleGetSer(queryset, many=True)
        return Response(s.data)

    def post(self, request):
        s = ScheduleSer(data=request.data)
        if s.is_valid():
            schedule = Schedule.objects.get_or_create(
                date = s.validated_data['data'],
                point = s.validated_data['point'],
                agent = s.validated_data['agent']
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)

    def put(self, request):
        s = ScheduleChangeSer(data=request.data)
        if s.is_valid():
            schedule = Schedule.objects.get(id=s.validated_data['id'])
            schedule.plan = s.validated_data.get('plan', schedule.plan)
            schedule.fact = s.validated_data.get('fact', schedule.fact)
            schedule.comments = s.validated_data.get('comments', schedule.comments)
            schedule.save()
            return Response({'status': 'ok'})

        else:   
            return Response(s.errors)



# class BasketApi(APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request):
#         queryset = Basket.objects.get(user=request.user)
#         s = BasketGetSer(queryset)
#         return Response(s.data)

#     def post(self, request):
#         s = BasketSer(data=request.data)
#         if s.is_valid():
#             b = Basket.objects.create(user=request.user)
#             products = s.validated_data['products']
#             for i in products:
#                 OrderProduct.objects.create(
#                     product = Product.objects.get(id=i['id']),
#                     count = i['count'],
#                     basket = b
#                 )
#             return Response({'status': 'ok'})
#         else:
#             return Response(s.errors)



