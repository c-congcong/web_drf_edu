from django.urls import path

from cart import views

urlpatterns = [
    path("option/", views.CartViewSet.as_view({"post": "add_cart",
                                               "get": "list_cart",
                                               "patch": "change_select",
                                               "put": "change_expire",
                                               })),
    path("option/<str:course>", views.CartViewSet.as_view({"delete": "del_course"})),
    path("option/change_all/", views.CartViewSet.as_view({"patch": "change_select_all"})),
]
