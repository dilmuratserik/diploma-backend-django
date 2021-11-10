from django.shortcuts import render
from rest_framework.views import APIView
import random
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import permissions
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
                apartment = s.validated_data['apartment'],
                floor = s.validated_data['floor'],
                entrance = s.validated_data['entrance'],
                user = request.user
            )
            return Response({'status': 'ok'})
        else:
            return Response({'status': 'error'})


class CountryApi(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        queryset = Country.objects.values('id', 'name').all()
        return Response(queryset)


class CityApi(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        queryset = City.objects.values('id', 'name', 'country').all()
        return Response(queryset)