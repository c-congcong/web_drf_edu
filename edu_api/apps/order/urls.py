from django.urls import path

from order import views

urlpatterns = [
    path("option/", views.OrderAPIView.as_view()),
    path("git_option/", views.GitOrderAPIView.as_view()),
    path("get/", views.OrderDetailAPIView.as_view()),
    path("del_order/<str:id>", views.DelOrderAPIView.as_view({"delete": "del_order"})),
    path("del_order/", views.DelOrderAPIView.as_view({"patch": "cha_order"})),
    path("get_list/", views.OrderListAPIView.as_view()),
]
