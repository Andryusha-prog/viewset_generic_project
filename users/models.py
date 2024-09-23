from django.contrib.auth.models import AbstractUser
from django.db import models


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
