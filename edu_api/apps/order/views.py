from rest_framework.generics import CreateAPIView, ListAPIView

from order.models import Order
from order.serializers import OrderModelSerializer, GitOrderModelSerializer, OrderDetailModelSerializer


class OrderAPIView(CreateAPIView):
    """生成订单"""
    queryset = Order.objects.filter(is_show=True, is_delete=False)
    serializer_class = OrderModelSerializer


class GitOrderAPIView(ListAPIView):
    """查询订单"""
    queryset = Order.objects.all().order_by("orders")
    serializer_class = GitOrderModelSerializer


class OrderDetailAPIView(ListAPIView):
    """查询订单"""
    queryset = Order.objects.all().order_by("orders")
    serializer_class = OrderDetailModelSerializer
