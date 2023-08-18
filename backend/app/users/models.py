from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model with email instead of username and OTP
    """
    username = None
    email = models.EmailField(verbose_name=_("email address"),
                              unique=True)
    USERNAME_FIELD = "email"
    # The field named as the 'USERNAME_FIELD' for a custom user model must not be included in 'REQUIRED_FIELDS'
    REQUIRED_FIELDS = []

    confirmation_otp = models.IntegerField(verbose_name=_("OTP"),
                                           null=True,
                                           blank=True)

    objects = CustomUserManager()
