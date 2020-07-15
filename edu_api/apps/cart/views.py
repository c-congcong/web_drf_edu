import logging

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from course.models import Course
from edu_api.settings import constants

log = logging.getLogger("django")


class CartViewSet(ViewSet):
    """购物车"""

    # 只有登录认证成功的才能访问接口
    # permission_classes = [IsAuthenticated]

    def add_cart(self, request):
        course_id = request.data.get("course_id")
        user_id = request.user.id
        # 是否勾选
        select = True
        # 有效期
        expire = 0

        # 校验参数  git匹配单个对象 ，filter是整个过滤返回querset
        try:
            Course.objects.get(is_show=True, id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取redis连接对象
            redis_connection = get_redis_connection("cart")
            # 保存到数据库
            pipeline = redis_connection.pipeline()
            # 开启管道
            pipeline.multi()
            # 商品信息对应有效期
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            # 被勾选的商品
            pipeline.sadd("selected_%s" % user_id, course_id)

            # 执行
            pipeline.execute()
            course_len = redis_connection.hlen("cart_%s" % user_id)
        except:
            log.error("购物车数据存储失败")
            return Response({"message": "参数有误，购物车添加失败"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"message": "购物车商品添加成功", "cart_length": course_len})

    def list_cart(self, request):
        """展示购物车"""
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall("cart_%s" % user_id)
        select_list_bytes = redis_connection.smembers("selected_%s" % user_id)
        # 循环从MySQL中找出商品信息
        data = []
        for course_id_bytes, expire_id_bytes in cart_list_bytes.items():
            course_id = int(course_id_bytes)
            expire_id = int(expire_id_bytes)

            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue

            data.append({
                "selected": True if course_id_bytes in select_list_bytes else False,
                "course_img": constants.IMG_SRC + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expire_id": expire_id,
                "price": course.price,
            })
        return Response(data)

    def change_select(self, request):
        """切换购物车商品状态"""
        user_id = request.user.id
        selected = request.data.get("selected")
        course_id = request.data.get("course_id")
        print(course_id,user_id)

        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，当前商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection("cart")
        if selected:
            redis_connection.sadd("selected_%s" % user_id, course_id)
        else:
            redis_connection.srem("selected_%s" % user_id, course_id)

        return Response({"message": "切换成功！"})

    def del_course(self, request):
        """删除商品"""
        user_id = request.user.id
        # user_id = 1
        course_id = request.data.get("course_id")
        redis_connection = get_redis_connection("cart")
        redis_connection.hdel("cart_%s" % user_id,course_id)
        print(course_id,user_id,redis_connection)

        return Response({"message": "删除成功！"})
