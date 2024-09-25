from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateApiView,
                             LessonDestroyApiView, LessonListApiView,
                             LessonRetrieveApiView, LessonUpdateApiView, PaymentListApiView, PaymentUpdateApiView)

app_name = MaterialsConfig.name


router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lesson_list"),
    path("lesson/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_detail"),
    path(
        "lesson/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/<int:pk>/destroy/", LessonDestroyApiView.as_view(), name="lesson_delete"
    ),
    path("payment/", PaymentListApiView.as_view(), name="payment_view"),
    path("payment/<int:pk>/update/", PaymentUpdateApiView.as_view(), name="payment_update"),
]

urlpatterns += router.urls
