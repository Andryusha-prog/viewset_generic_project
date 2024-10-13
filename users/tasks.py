from datetime import datetime

from celery import shared_task
from dateutil.relativedelta import relativedelta

from users.models import User


@shared_task
def check_user_last_login():
    now_date = datetime.now()
    date_minus_month = now_date + relativedelta(months=-1)
    users = User.objects.filter(last_login__lt=date_minus_month, is_active=True)
    print(users)
    for user in users:
        user.is_active = False
        user.save()

    # user = User.objects.get(email='alhimik23@mail.ru')
    # print(user.is_active)
    # if user.is_active is False:
    #     user.is_active = True
    #     user.save()