from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from user import views

urlpatterns = [
    path("login/", obtain_jwt_token),
    path("captcha/", views.CaptchaAPIView.as_view()),
    path("register/", views.UserAPIView.as_view()),
    path("sms_login/", views.SmsLoginAPIView.as_view()),
    path("mobile/<str:mobile>", views.MobileCheckAPIView.as_view()),
    path("mobile1/<str:mobile>", views.MobileAPIView.as_view()),
    path("sms/<str:mobile>", views.SendMessageAPIView.as_view()),
]
