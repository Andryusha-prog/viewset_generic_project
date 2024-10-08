import re

from rest_framework.exceptions import ValidationError


class UrlCustomValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        '''reg_exp = re.compile('.*:\/\/youtube.com\/.*')
        url_data = dict(value).get(self.field)
        if not bool(reg_exp.match(url_data)):
            raise ValidationError('запрещено размещать ссылки на сторонние ресурсы, кроме youtube.com')
            '''
        video_url = value.get(self.field)
        if video_url and not video_url.startswith('https://www.youtube.com/'):
            raise ValidationError('Ой, ссылка не на Ютуб. Сорри, ее не получится прикрепить :(')

