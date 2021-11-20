from django.shortcuts import render
from rest_framework import pagination
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
    filter_fields = ('category', 'subcategory')
    
    def get_queryset(self):
        minheight = self.request.GET.get('minprice')
        maxheight = self.request.GET.get('maxprice')
        if(minheight and maxheight):
            return self.queryset.filter(price__gte=minheight, price__lte=maxheight)
        return self.queryset

class CreateProduct(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = getProductSer(data=request.data)
        if s.is_valid():
            # print(dict(s.validated_data.get('data', None)[0]))
            # print(s.validated_data.get('data', None))
            data = s.validated_data.get('data', None)
            for i in data:
                # print('iii', type(i))
                # i = eval(i)
                p = Product.objects.filter(code = i['code'])
                if p.exists():
                    print(i['code'])
                else:
                    p = Product.objects.create(
                        code = i['code'],
                        name = i['name'],
                        price = i['price']
                    )
                    if 'uuid' in i:
                        p.uuid = i['uuid']
                    if 'description' in i:
                        p.description = i['description']
                    if 'articul' in i:
                        p.articul = i['articul']
                    if 'unit' in i:
                        p.unit = i['unit']
                    if 'count' in i:
                        p.count = i['count']
                    p.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class GetProductCode(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request, code):
        s = ProductGetSer(data=request.data)
        if s.is_valid():
            p = Product.objects.filter(code = code)
            if p.exists():
                p = p[0]
                price = s.validated_data.get('price', None)
                if price:
                    p.price = price
                name = s.validated_data.get('name', None)
                if name:
                    p.name = name
                articule = s.validated_data.get('articul', None)
                if articule:
                    p.articul = articule
                p.save()
                return Response({'status': 'ok'})
            else:
                return Response({'status': 'not found'})
        else:
            return Response(s.errors)


class HitsApi(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    queryset = Product.objects.all().order_by("-count_order")[:4]
    serializer_class = productSer
    pagination_class = None


class RecommendationApi(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    queryset = Product.objects.all().order_by("?")[:4]
    serializer_class = productSer
    pagination_class = None


