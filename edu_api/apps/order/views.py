from rest_framework.generics import CreateAPIView

from order.models import Order
from order.serializers import OrderModelSerializer


class OrderAPIView(CreateAPIView):
    """生成订单"""
    queryset = Order.objects.filter(is_show=True, is_delete=False)
    serializer_class = OrderModelSerializer
