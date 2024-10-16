from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import ListViewPaginator
from materials.serializers import (CourseDetailSerializer, CourseSerializer,
                                   LessonSerializer, PaymentSerializer,
                                   SubscribeSerializer)
from materials.services import create_stripe_price, create_stripe_session
from materials.task import send_mail_info_update
from users.models import Payment, User
from users.permissions import IsModerators, IsOwner


# Create your views here.
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = ListViewPaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ("update", "retrieve"):
            self.permission_classes = (IsModerators | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner,)
        elif self.action == "create":
            self.permission_classes = (~IsModerators,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        data = serializer.save()
        course_id = data.pk
        users_pk = [x['user'] for x in Subscription.objects.values('user').filter(course=course_id)]
        users_mail = [mail['email'] for mail in User.objects.values('email').filter(pk__in=users_pk)]
        send_mail_info_update(users_mail, data.name)
        data.save()

class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerators]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = ListViewPaginator


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerators | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerators | IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = (
        "pay_course",
        "pay_lesson",
        "pay_type",
    )
    ordering_fields = ("pay_date",)


class PaymentUpdateApiView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentCreateApiView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if "course" in self.request.data:
            course = Course.objects.get(pk=self.request.data["course"])
            payment.pay_course = course

        if "lesson" in self.request.data:
            lesson = Lesson.objects.get(pk=self.request.data["lesson"])
            payment.pay_lesson = lesson

        price = create_stripe_price(payment.price)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()



class SubscribeApiView(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["course", "user"],
            properties={
                "course": openapi.Schema(type=openapi.TYPE_INTEGER),
                "user": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="подписка добавлена или подписка удалена",
                    )
                },
            )
        },
    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        # Возвращаем ответ в API
        return Response({"message": message})


class SubscribeListApiView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer
