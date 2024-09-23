from django.db import models


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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.name}"
