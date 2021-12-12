from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets, generics, status
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework import filters
from rest_framework.decorators import permission_classes



class TypePriceApi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Type_Price.objects.all()
    serializer_class = TypePriceSer
    pagination_class = None


class OrderSectorApi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Order_Sector.objects.all()
    serializer_class = OrderSectorSer
    pagination_class = None
