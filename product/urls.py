from django.urls import path, include
from product import views

urlpatterns = [
    path('', views.getProduct.as_view({'get': 'list'})),
    path('unload/', views.GetProduct.as_view()),
    path('unload/<code>', views.GetProduct.as_view()),
]