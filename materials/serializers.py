from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import UrlCustomValidator
from users.models import Payment


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlCustomValidator(field="video_url")]


class CourseDetailSerializer(ModelSerializer):
    count_lesson_on_course = SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set.all", many=True)
    subscription_sign = SerializerMethodField()

    def get_count_lesson_on_course(self, course):
        return Lesson.objects.filter(course=course.pk).count()

    def get_subscription_sign(self, course):
        user_pk = self.context["request"].user.pk
        return Subscription.objects.filter(course=course.pk, user=user_pk).exists()

    class Meta:
        model = Course
        fields = (
            "name",
            "description",
            "count_lesson_on_course",
            "lesson",
            "subscription_sign",
        )


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscribeSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
