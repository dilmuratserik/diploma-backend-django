from django.shortcuts import render
from rest_framework.views import APIView
import random
from .serializers import *
from .models import Product
from locations.models import Country, City
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveUpdateAPIView
from datetime import datetime
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination # Any other type works as well


class getProduct(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    queryset = Product.objects.all()
    serializer_class = productSer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # pagination_class = PageNumberPagination
    search_fields = ('name', 'description')
    filter_fields = ('category',)
    
    def get_queryset(self):
        minheight = self.request.GET.get('minprice')
        maxheight = self.request.GET.get('maxprice')
        if(minheight and maxheight):
            return self.queryset.filter(price__gte=minheight, price__lte=maxheight)
        return self.queryset