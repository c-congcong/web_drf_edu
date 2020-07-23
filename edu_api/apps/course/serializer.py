from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategorySerializer(ModelSerializer):
    """课程分类"""

    class Meta:
        model = CourseCategory
        fields = ["id", "name"]


class CourseLessonModelSerializer(ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ("id", "name", "free_trail", "duration")


class CourseChapterModelSerializer(ModelSerializer):
    """章节列表"""

    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ["id", "name", "chapter", "coursesections"]


class CourseTeacherSerializer(ModelSerializer):
    """课程所属老师的序列化器"""

    class Meta:
        model = Teacher
        fields = ("id", "name", "title", "signature", "role", "image")


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    # 序列化器嵌套查询老师信息
    teacher = CourseTeacherSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", "lesson_list",
                  "course_type", "course_video", "brief_html", "level_name", "discount_name",
                  "real_price", "active_time", "expire_list"]
