from django.urls import path, include
from . import views

urlpatterns = [
    path('my/address/', views.AddressView.as_view()),
    path('country/list/', views.CountryApi.as_view()),
    path('city/list/', views.CityApi.as_view())
]