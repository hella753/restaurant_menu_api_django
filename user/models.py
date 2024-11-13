from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password, **other_fields):
        if not username:
            raise ValueError("Required Field username is not set")
        if not password:
            raise ValueError("Required Field password is not set")
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **other_fields):
        if not username:
            raise ValueError("Required Field username is not set")
        if not password:
            raise ValueError("Required Field password is not set")
        user = self.create_user(username, password, **other_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=20,
        unique=True,
        help_text="Required. 20 characted or fewer.",
        error_messages={
            "unique": "A user with that username already exists."
        },
        verbose_name=_("მომხმარებლის სახელი")
    )
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("ელ. ფოსტა")
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("შექმნის თარიღი")
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("სახელი")
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("გვარი")
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
        verbose_name=_("სტაფის სტატუსი")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("აქტიურობის სტატუსი")
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"
