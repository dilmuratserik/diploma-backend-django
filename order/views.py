from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from product.models import Product
from .serializers import *
from .models import *
from locations.models import Address, Country, City, Outlets, Storage_region
from users.models import User
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets, generics, status
# import random
# from datetime import date, datetime
# from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import PageNumberPagination 


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
        from collections import OrderedDict
        if s.is_valid():
            if type(s.validated_data) == OrderedDict:
                vd = dict(s.validated_data)
            else:
                vd = s.validated_data
            address_id = s.validated_data.get('delivery_address', None)
            address = None
            if address_id:
                address = Address.objects.get(id=address_id)
            paddress = None
            paddress_id = s.validated_data.get('pickup_address', None)
            if paddress_id:
                paddress = Storage_region.objects.get(id=paddress_id)
            user = User.objects.get(id=vd['counterparty'])
            order = Order.objects.create(
                type_delivery = vd.get('type_delivery', 1),
                counterparty = user,
                delivered_date = vd.get('delivered_date', None),
                delivery_address = address,
                pickup_address = paddress
            )
            products = vd['products']
            for i in products:
                p = Product.objects.get(id=i['id'])
                OrderProduct.objects.create(
                    product = p,
                    count = i['count'],
                    order = order
                )
                p.count_order += 1
                p.save()
            bonus = s.validated_data.get('bonus', None)
            if bonus:
                user.bonus = 0
            user.bonus = order.total * 0.1
            user.save()
            return Response({'status': "ok"})
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class CourierOrderHistory(APIView):
    permission_classes = (permissions.IsAuthenticated,)

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
            schedule = Schedule.objects.create(
                date = s.validated_data['date'],
                point = s.validated_data['point'],
                agent = s.validated_data['agent']
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class IndividualHistoryApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Order.objects.filter(counterparty=request.user)
        s = OrderSer(queryset, many=True)
        return Response(s.data)

class CourierOrderChange(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = CourierOrderSer(data=request.data)
        if s.is_valid():
            order = Order.objects.get(id=s.validated_data['id'])
            comment = s.validated_data.get('comment', None)
            if comment:
                order.comment = comment
            status = s.validated_data.get('status', None)
            if status:
                order.status = status
            date = s.validated_data.get('date', None)
            if date:
                order.delivered_date = date
            order.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderAllApi(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSer
    filter_fields = ('counterparty', 'status', 'courier', 'delivered_date', 'date')

class AddCourierToOrder(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = AddCourierToOrderSer(data=request.data)
        if s.is_valid():
            order = Order.objects.get(id=s.validated_data['order_id'])
            courier = User.objects.get(id=s.validated_data['courier_id'])
            order.courier = courier
            order.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class listSchedule(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Schedule.objects.all()
    serializer_class = ScheduleGetSer
    filter_fields = ('agent', 'point', 'date')

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



