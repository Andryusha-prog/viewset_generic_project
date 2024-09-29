from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(
        verbose_name="email", help_text="Введите свой email", unique=True
    )
    phone = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        help_text="Введите ваш номер телефона",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="город",
        help_text="Введите свой город",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatar",
        verbose_name="аватар",
        help_text="Загрузите свой аватар",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Оплативший пользователь",
        blank=True,
        null=True,
    )
    pay_date = models.DateField(verbose_name="дата оплаты", blank=True, null=True)
    pay_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный курс",
        blank=True,
        null=True,
    )
    pay_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный урок",
        blank=True,
        null=True,
    )
    price = models.IntegerField(verbose_name="сумма оплаты", blank=True, null=True)
    pay_type = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.price} - {self.user} - {self.pay_date}"
