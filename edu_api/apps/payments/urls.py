from django.urls import path

from payments import views

urlpatterns = [
    path("pay/", views.AliPayAPIView.as_view()),
    path("pay1/", views.AliPayResultAPIView.as_view()),
]
