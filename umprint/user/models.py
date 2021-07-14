import uuid

from django.db import models


class UserProfile(models.Model):
    REQUIRED_FIELDS = ('id', 'telegram_login', 'email')
    USERNAME_FIELD = 'login'
    is_anonymous = False
    is_authenticated = True
    is_active = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(max_length=20, blank=True, unique=True, verbose_name='Логин')
    telegram_login = models.CharField(max_length=100, blank=True, unique=True, verbose_name='Телеграм логин')
    password = models.CharField(max_length=20, blank=True, verbose_name='Пароль')
    first_name = models.CharField(max_length=20, blank=True, verbose_name='Имя')
    second_name = models.CharField(max_length=20, blank=True, verbose_name='Фамилия')
    email = models.EmailField(max_length=20, blank=True, unique=True, verbose_name='Почта')

    def __unicode__(self):
        return self.login
