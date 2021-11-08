from django.urls import path
from . import views

urlpatterns = [
    path('category/list/', views.CategoryApi.as_view()),
    path('subcategory/list/', views.SubCategoryApi.as_view())
]