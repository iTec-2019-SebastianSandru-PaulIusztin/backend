from django.contrib.auth.models import AbstractUser as DjangoAbstractUser
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.authentication.utils import get_photos_path_creator


class UserManager(DefaultUserManager):
    def create_superuser(self, email, password, username=None, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)


class AbstractUser(DjangoAbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    photo = models.ImageField(
        upload_to=get_photos_path_creator(field_name="photo"),
        blank=True,
        null=True,
        max_length=255,
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "auth_user"
        abstract = True

    @property
    def is_first_login(self):
        return self.date_joined == self.last_login
