from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', views.OrderApi.as_view()),
    path('api/', views.CreateOrderApi.as_view()),
    path('courier/', views.CourierOrderHistory.as_view()),
    path('plan/', views.ScheduleApi.as_view()),
    path('history/', views.IndividualHistoryApi.as_view()),
    path('courier/order/change/', views.CourierOrderChange.as_view()),

    path('admin/', views.OrderAllApi.as_view({'get': 'list'})),
    path('add/courier/', views.AddCourierToOrder.as_view()),

    path('schedule/list/', views.listSchedule.as_view({'get': 'list'}))
    # path('basket/', views.BasketApi.as_view())
]
