from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    class UserKind(models.TextChoices):
        VISITOR = 'Visitor', _('Visitor')
        INSPECTOR = 'Inspector', _('Inspector')
        SUPERVISOR = 'Supervisor', _('Supervisor')
        ADMIN = 'Admin', _('Admin')

    kind = models.CharField(max_length=32, choices=UserKind.choices, default=UserKind.VISITOR)


class Inspector(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Supervisor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
