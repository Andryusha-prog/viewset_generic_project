from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, PaymentSerializer
from users.models import Payment


# Create your views here.
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    #serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter]

    filterset_fields = ("pay_course", "pay_lesson", "pay_type",)
    ordering_fields = ("pay_date",)




class PaymentUpdateApiView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

