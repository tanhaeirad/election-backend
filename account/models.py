# TODO: zone should be change and refer to zone model

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

    # def _is_inspector(self):
    #     try:
    #         obj = Inspector.objects.get(pk=self.pk)
    #
    #     except Inspector.DoesNotExist:
    #         obj = None
    #
    #     finally:
    #         return bool(obj)
    #
    # def _is_supervisor(self):
    #     try:
    #         obj = Supervisor.objects.get(pk=self.pk)
    #
    #     except Supervisor.DoesNotExist:
    #         obj = None
    #
    #     finally:
    #         return bool(obj)
    #
    # def _is_admin(self):
    #     try:
    #         obj = Admin.objects.get(pk=self.pk)
    #
    #     except Admin.DoesNotExist:
    #         obj = None
    #
    #     finally:
    #         return bool(obj)


class Inspector(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zone = models.IntegerField()


class Supervisor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zone = models.IntegerField()


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
