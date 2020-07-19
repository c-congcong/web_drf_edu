import logging

from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from course.models import Course, CourseExpire
from edu_api.settings import constants

log = logging.getLogger("django")


class CartViewSet(ViewSet):
    """购物车"""

    # 只有登录认证成功的才能访问接口
    permission_classes = [IsAuthenticated]

    def add_cart(self, request):
        course_id = request.data.get("course_id")
        print(course_id)
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
                # "price": course.price,
                # 购物车列表需要课程有效期
                "expire_list": course.expire_list,
                # TODO 获取真实价格
                "real_price": course.real_expire_price(expire_id),
            })
        return Response(data)

    def change_select(self, request):
        """切换购物车商品状态"""
        user_id = request.user.id
        selected = request.data.get("selected")
        course_id = request.data.get("course_id")
        print(course_id, user_id, selected)

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

    def change_select_all(self, request):
        """切换购物车商品状态"""
        user_id = request.user.id
        selected = request.data.get("selected")
        course_id = request.data.get("course_id")
        print(course_id, user_id, selected)

        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，当前商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection("cart")
        if selected:
            redis_connection.srem("selected_%s" % user_id, course_id)
        else:
            redis_connection.sadd("selected_%s" % user_id, course_id)

        return Response({"message": "切换成功！"})

    def del_course(self, request, *args, **kwargs):
        """删除商品"""
        user_id = request.user.id
        course_id = kwargs.get("course")
        print(course_id)
        redis_connection = get_redis_connection("cart")
        redis_connection.hdel("cart_%s" % user_id, course_id)
        print(course_id, user_id, redis_connection)

        return Response({"message": "删除成功！"})

    def change_expire(self, request):
        """改变redis中课程的有效期"""
        user_id = request.user.id
        expire_id = request.data.get("expire_id")
        course_id = request.data.get("course_id")
        print(course_id, expire_id)

        try:
            course = Course.objects.get(is_show=True, is_delete=False, id=course_id)
            # 如果前端传递来的有效期选项  如果不是0  则修改课程对应的有效期
            if expire_id > 0:
                expire_iem = CourseExpire.objects.filter(is_show=True, is_delete=False, id=expire_id)
                if not expire_iem:
                    raise Course.DoesNotExist()
        except Course.DoesNotExist:
            return Response({"message": "课程信息不存在"}, status=status.HTTP_400_BAD_REQUEST)

        connection = get_redis_connection("cart")
        connection.hset("cart_%s" % user_id, course_id, expire_id)

        # 重新计算切换有效期后的价钱
        real_price = course.real_expire_price(expire_id)

        return Response({"message": "切换有效期成功", "real_price": real_price})

    def get_select_course(self, request):
        """
        获取购物车中已勾选的商品  返回前端所需的数据
        """

        user_id = request.user.id
        redis_connection = get_redis_connection("cart")

        # 获取当前登录用户的购车中所有的商品
        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        select_list = redis_connection.smembers("selected_%s" % user_id)

        total_price = 0  # 商品总价
        data = []

        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            print(course_id, expire_id)

            # 判断商品id是否在已勾选的的列表中
            if course_id_byte in select_list:
                try:
                    # 获取到的所有的课程信息
                    course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                except Course.DoesNotExist:
                    continue
                # 如果有效期的id大于0  则需要计算商品的价格  id不大于0则代表永久有效 需要默认值
                original_price = course.price
                expire_text = "永久有效"

                try:
                    if expire_id > 0:
                        course_expire = CourseExpire.objects.get(id=expire_id)
                        # 对应有效期的价格
                        original_price = course_expire.price
                        expire_text = course_expire.expire_text
                except CourseExpire.DoesNotExist:
                    pass

                # 根据已勾选的商品的对应有效期的价格去计算勾选商品的最终价格
                real_expire_price = course.real_expire_price(expire_id)

                # 将购物车所需的信息返回
                data.append({
                    "course_img": constants.IMG_SRC + course.course_img.url,
                    "name": course.name,
                    "id": course.id,
                    "expire_text": expire_text,
                    # 经过活动计算完成后的真实价格
                    "real_price": "%.2f" % float(real_expire_price),
                    # 原价
                    "price": original_price,
                    # 活动名称
                    "discount_name": course.discount_name,
                })

                # 商品总价
                total_price += float(real_expire_price)

        return Response({"course_list": data, "total_price": total_price, "message": '获取成功'})
