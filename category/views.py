from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from rest_framework import permissions
from rest_framework.decorators import permission_classes


class CategoryApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = Category.objects.values('id', 'name').all()
        return Response(queryset)


class SubCategoryApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = SubCategory.objects.values('id', 'name', 'category').all()
        return Response(queryset)

