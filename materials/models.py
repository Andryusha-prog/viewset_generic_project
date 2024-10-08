from django.db import models

from config.settings import AUTH_USER_MODEL


# Create your models here.
class Course(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="название", help_text="Введите название"
    )
    preview = models.ImageField(
        upload_to="materials/course/preview",
        null=True,
        blank=True,
        help_text="Загрузите превью курса",
        verbose_name="Превью курса",
    )
    description = models.TextField(
        verbose_name="описание курса",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Создатель"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return f"{self.name}"


class Lesson(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="название", help_text="введите название урока"
    )
    description = models.TextField(
        verbose_name="описание урока",
        blank=True,
        null=True,
        help_text="Введите описание урока",
    )
    preview = models.ImageField(
        upload_to="materials/lesson/preview",
        null=True,
        blank=True,
        help_text="Загрузите превью урока",
        verbose_name="Превью урока",
    )
    video_url = models.URLField(
        max_length=200,
        verbose_name="URL видео",
        help_text="Введите url видео",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="курс",
        help_text="выберите курс",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Создатель"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.name}"


class Subscription(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Курс')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} - {self.course}"

