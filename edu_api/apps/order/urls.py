from django.urls import path

from order import views

urlpatterns = [
    path("option/", views.OrderAPIView.as_view()),
    path("get_option/", views.GitOrderAPIView.as_view()),
    path("get/", views.OrderDetailAPIView.as_view()),
]
