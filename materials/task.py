from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_mail_info_update(users_mail, course_name):
    send_mail(
        subject='обновление курса',
        message=f'курс {course_name} обновлен',
        from_email=EMAIL_HOST_USER,
        recipient_list=users_mail
    )