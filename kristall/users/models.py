from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator, PhoneValidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    roles = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )
    username_validator = UsernameValidator()
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    email = models.EmailField('Email', max_length=254, unique=True)
    phone = models.IntegerField(
        'Телефон +7(ХХХ) ХХХ ХХ ХХ',
        blank=True,
        null=True,
        validators=[PhoneValidator()],
        )
    role = models.CharField(
        'Роль пользователя',
        choices=roles,
        max_length=max(len(role[1]) for role in roles), default=USER
    )

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELDS = 'email'

    def __str__(self):
        return str(self.username)

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"
