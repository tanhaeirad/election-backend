from django.db import models

from account.models import User


class City(models.Model):
    name = models.CharField(max_length=255)
