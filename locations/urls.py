from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'storage', views.StorageRegionApi, basename='address')

urlpatterns = [
    path('my/address/', views.AddressView.as_view()),
    path('my/address/change/<id>', views.changeAddress.as_view()),
    path('country/list/', views.CountryApi.as_view()),
    # path('city/list/', views.CityApi.as_view())
]
urlpatterns += router.urls
