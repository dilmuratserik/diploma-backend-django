from django.urls import path, include
from . import views

urlpatterns = [
    path('my/address/', views.AddressView.as_view())
]