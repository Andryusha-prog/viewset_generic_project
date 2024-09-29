from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_list = [
            {"email": "user_test1@mail_test.ru"},
            {"email": "user_test2@mail_test.ru"},
        ]
        payment_list = [
            {
                "user": User.objects.get(pk=1),
                "pay_course": Course.objects.get(pk=2),
                "price": 20000,
            },
            {
                "user": User.objects.get(pk=2),
                "pay_lesson": Lesson.objects.get(pk=3),
                "price": 5000,
            },
        ]

        for user in user_list:
            User.objects.create(**user)

        for pay in payment_list:
            Payment.objects.create(**pay)
