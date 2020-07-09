from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView

from edu_api.settings.constants import BANNER_LENGTH, NAV_LENGTH
from home.models import Banner, Nav
from home.serializers import BannerModelSerializer,FooterModelSerializer


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("-orders")[:BANNER_LENGTH]
    serializer_class = BannerModelSerializer


# class HeaderListAPIView(ListAPIView):
#     """导航菜单"""
#     queryset = Nav.objects.filter(is_show=True, is_delete=False).order_by("-orders")[:NAV_LENGTH]
#     serializer_class = NavModelSerializer

class FooterListAPIView(ListAPIView):
    # 查询底部的数据position=2
    queryset = Nav.objects.filter(position=2)
    serializer_class = FooterModelSerializer


class HeaderListAPIView(ListAPIView):
    # 查询顶部的数据position=1
    queryset = Nav.objects.filter(position=1)
    serializer_class = FooterModelSerializer
