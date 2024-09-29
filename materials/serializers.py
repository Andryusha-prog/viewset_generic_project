from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from users.models import Payment


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson_on_course = SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set.all", many=True)

    def get_count_lesson_on_course(self, course):
        return Lesson.objects.filter(course=course.pk).count()

    class Meta:
        model = Course
        fields = ("name", "description", "count_lesson_on_course", "lesson")


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
