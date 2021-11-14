from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', views.OrderApi.as_view()),
    path('api/', views.CreateOrderApi.as_view()),
    path('courier/', views.CourierOrderHistory.as_view()),
    path('plan/', views.ScheduleApi.as_view())
    # path('basket/', views.BasketApi.as_view())
]
