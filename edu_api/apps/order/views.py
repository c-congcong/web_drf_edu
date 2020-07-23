from datetime import datetime

from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from order.models import Order, OrderDetail
from order.serializers import OrderModelSerializer, GitOrderModelSerializer, OrderDetailModelSerializer


class OrderAPIView(CreateAPIView):
    """生成订单"""
    # 只有登录认证成功的才能访问接口
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.filter(is_show=True, is_delete=False)
    serializer_class = OrderModelSerializer


class GitOrderAPIView(ListAPIView):
    """查询订单"""
    # 只有登录认证成功的才能访问接口
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all().order_by("orders")
    serializer_class = GitOrderModelSerializer


class OrderDetailAPIView(ListAPIView):
    """查询订单详细"""
    # 只有登录认证成功的才能访问接口
    permission_classes = [IsAuthenticated]
    queryset = OrderDetail.objects.all().order_by("orders")
    serializer_class = OrderDetailModelSerializer


class DelOrderAPIView(ViewSet):
    """删除订单"""
    # 只有登录认证成功的才能访问接口
    permission_classes = [IsAuthenticated]

    def del_order(self, request, *args, **kwargs):
        """删除商品"""
        try:
            id = kwargs.get("id")
            Order.objects.get(pk=id).delete()
        except:
            return Response({"message": "删除失败！"})

        return Response({"message": "删除成功！"})

    def cha_order(self, request, *args, **kwargs):
        """删除商品"""
        try:
            id = kwargs.get("id")
            print(id)
            order = Order.objects.get(pk=id)
            order.order_status = 2
            order.save()
        except:
            return Response({"message": "失败！"})

        return Response({"message": "取消成功！"})


class OrderListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # id = kwargs.get("id")
        # 调用定时函数
        # 通过celery异步执行发送短信的服务
        from my_task.change_order.tasks import check_order
        # 调用任务函数  发布任务
        check_order.delay()  # 如果需要参数则传递过去 不需要则不传递
        return Response("11")
