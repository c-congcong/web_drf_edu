from django.urls import path

from cart import views

urlpatterns = [
    path("option/", views.CartViewSet.as_view({"post": "add_cart",
                                               "get": "list_cart",
                                               "patch": "change_select",
                                               "delete": "del_course"})),
]
