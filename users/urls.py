from django.urls import path, include
from users import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'detail', views.detailUser2, basename='users')
router.register(r'tp', views.TPUserView, basename='tp')
# router.register(r'courier', views.CourierUserView, basename='courier')

urlpatterns = [
    path('login/', views.Logined.as_view()),
    path('phone/otp/', views.PhoneCode.as_view()),
    path('register/', views.Register.as_view()),
    path('register/continue/', views.RegisterationContinue.as_view()),

    path('get/detail/<id>', views.detailUser.as_view()),
    path('point/list/', views.GetPointListApi.as_view()),
    # path('detail', views.detailUser2.as_view()),
    path('password/change/', views.PasswordChangeView.as_view()),
    path('change/ava/', views.Avatar.as_view()),

    path('points/', views.GetPointDetailApi.as_view()),

    path('courier/list/', views.CourierListApi.as_view()),
]
urlpatterns += router.urls
