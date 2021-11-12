from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', views.OrderApi.as_view()),
    path('basket/', views.BasketApi.as_view())
]
