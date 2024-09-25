from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from users.models import Payment


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson_on_course = SerializerMethodField()
    lesson = SerializerMethodField()

    def get_lesson(self, course):
        return [les.name for les in Lesson.objects.filter(course=course)]

    def get_count_lesson_on_course(self, course):
        return Lesson.objects.filter(course=course.pk).count()

    class Meta:
        model = Course
        fields = ("name", "description", "count_lesson_on_course", "lesson")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
