from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)


class Zone(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
