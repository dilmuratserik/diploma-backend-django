from django.urls import path, include
from product import views

urlpatterns = [
    path('', views.getProduct.as_view({'get': 'list'})),
    path('unload/', views.CreateProduct.as_view()),
    path('unload/<code>', views.GetProductCode.as_view()),

    path('hits/', views.HitsApi.as_view({'get': 'list'})),
    path('recommendation/', views.RecommendationApi.as_view({'get': 'list'}))
]