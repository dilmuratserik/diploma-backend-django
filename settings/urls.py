from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'price/type', views.TypePriceApi, basename='pricetype')
router.register(r'order/sector', views.OrderSectorApi, basename='pricetype')


urlpatterns = [
    # path('login/', views.Logined.as_view()),
   
]
urlpatterns += router.urls
