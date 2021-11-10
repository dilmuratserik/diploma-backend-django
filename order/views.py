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
from datetime import datetime
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

    def post(self, request):
        s = orderCreateSer(data=request.data)
        if s.is_valid():
            order = Order.objects.create(
                outlet = Outlets.objects.get(s.validated_data['outlet']),
                counterparty = User.objects.get(['counterparty'])
            )
            products = s.validated_data['products']
            for i in products:
                OrderProduct.objects.create(
                    product = Product.objects.get(id=i['id']),
                    count = i['count'],
                    order = order
                )
            return Response({'status': "ok"})
        else:
            return Response(s.errors)
