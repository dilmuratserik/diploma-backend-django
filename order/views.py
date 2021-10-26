from django.shortcuts import render
from rest_framework.views import APIView
import random
from .serializers import *
from .models import *
from locations.models import Country, City
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveUpdateAPIView
from datetime import datetime
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination 


class OrderApi(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        o = Order.objects.all()
        s = OrderSer(o, many=True)
        return Response(s.data)