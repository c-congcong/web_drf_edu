from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from edu_api.utils.response import APIResponse

from course.models import CourseCategory, Course, Teacher, CourseLesson, CourseChapter
from course.pagination import CoursePageNumber
from course.serializer import CourseCategorySerializer, CourseModelSerializer, CourseChapterModelSerializer


class   CourseCategoryListAPIView(ListAPIView):
    """课程分类信息查询"""
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseCategorySerializer


class CourseListAPIView(ListAPIView):
    """课程列表查询"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer


class CourseFilterListAPIView(ListAPIView):
    """根据条件查询课程"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer

    # 根据不同的分类id查询不同的课程
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course_category",)
    # 排序
    ordering_fields = ("id", "students", "price")
    # 分页   只能有一个
    pagination_class = CoursePageNumber


class CourseNameListAPIView(RetrieveAPIView):
    """课程本身信息查询"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer
    lookup_field = 'id'


class CourseChapterListAPIView(ListAPIView):
    """课程章节信息查询"""
    queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["course"]

