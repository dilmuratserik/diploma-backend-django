from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.CategoryApi.as_view()),
    # path('subcategory/list/', views.SubCategoryApi.as_view())
]