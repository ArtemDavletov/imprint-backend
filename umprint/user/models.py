import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from django.utils import timezone


class UserProfile(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    REQUIRED_FIELDS = ("id", "telegram_login", "email")
    is_anonymous = False
    is_authenticated = True
    is_active = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_staff = models.BooleanField(default=False, verbose_name="Статус персонала?")
    is_active = models.BooleanField(default=True, verbose_name="Активный пользователь?")
    date_joined = models.DateTimeField(default=timezone.now)
    login = models.CharField(
        max_length=40, blank=True, unique=True, verbose_name="Логин"
    )
    telegram_login = models.CharField(
        max_length=100, blank=True, unique=True, verbose_name="Телеграм логин"
    )
    password = models.CharField(max_length=100, blank=True, verbose_name="Пароль")
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Имя")
    second_name = models.CharField(max_length=100, blank=True, verbose_name="Фамилия")
    email = models.EmailField(
        max_length=200, blank=True, unique=True, verbose_name="Почта"
    )
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "login"
    objects = CustomUserManager()

    def __unicode__(self):
        return self.login
