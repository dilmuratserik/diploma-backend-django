from django.db.models.query import QuerySet
from django.http import request
from django.shortcuts import render
from rest_framework.views import APIView
import random
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.decorators import permission_classes
from rest_framework import viewsets, generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView, RetrieveUpdateAPIView
from datetime import datetime

class AddressView(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        queryset = Address.objects.filter(user=request.user)
        ser = AddressSer(queryset, many=True)
        return Response(ser.data)

    def post(self, request):
        s = AddressSer(data=request.data)
        if s.is_valid():
            a = Address.objects.create(
                street = s.validated_data['street'],
                house = s.validated_data['house'],
                apartment = s.validated_data.get('apartment', None),
                floor = s.validated_data.get('floor', None),
                entrance = s.validated_data.get('entrance', None),
                lat = s.validated_data.get('lat', None),
                lng = s.validated_data.get('lng', None),
                user = request.user
            )
            return Response({'status': 'ok'})
        else:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        s = IdSer(data=request.data)
        if s.is_valid():
            address = Address.objects.filter(id=s.validated_data['id'])
            if address.exists():
                address.first().delete()
                return Response({'status': 'ok'})
            else:
                return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class changeAddress(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def put(self, request, id):
        s = AddressSer(data=request.data)
        if s.is_valid():
            address = Address.objects.filter(id=id)
            if address.exists():
                address = address.first()
                address.street = s.validated_data.get('street', address.street)
                address.house = s.validated_data.get('house', address.house)
                address.apartment = s.validated_data.get('apartment', address.apartment)
                address.floor = s.validated_data.get('floor', address.floor)
                address.entrance = s.validated_data.get('entrance', address.entrance)
                address.lat = s.validated_data.get('lat', address.lat)
                address.lng = s.validated_data.get('lng', address.lng)
                address.save()
                return Response({'status': 'ok'})
            else:
                return Response({'status': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class CountryApi(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        queryset = Country.objects.values('id', 'name').all()
        queryset2 = City.objects.values('id', 'name', 'country').all()
        return Response({'country': queryset, 'city': queryset2})

class StorageRegion(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        queryset = Storage_region.objects.values('id', 'name').all()
        return Response(queryset)


# class CityApi(APIView):
#     permission_classes = [permissions.AllowAny,]

#     def get(self, request):
#         queryset = City.objects.values('id', 'name', 'country').all()
#         return Response(queryset)