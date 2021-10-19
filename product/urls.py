from django.urls import path, include
from product import views

urlpatterns = [
    path('', views.getProduct.as_view({'get': 'list'}))
]