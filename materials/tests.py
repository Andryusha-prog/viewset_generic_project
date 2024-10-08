from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscription
from users.models import User


# Create your tests here.
class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user_test@mail.ru")
        self.lesson = Lesson.objects.create(name="test lesson", description="lesson for check test", owner=self.user)
        self.course = Course.objects.create(name="test course", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        #print(data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "name": "first less"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )


    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "less"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        #print(data)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": self.lesson.preview,
                    "video_url": self.lesson.video_url,
                    "course": None,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            data, result
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@mail.ru")
        self.course = Course.objects.create(name="test course")
        self.subs = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subs(self):
        url = reverse("materials:subscribe")
        data = {
            "user": self.user.pk,
            "course": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.json(), {"message": "подписка удалена"}
        )

