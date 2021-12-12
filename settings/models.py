from django.core.exceptions import MiddlewareNotUsed
from django.db import models


class Type_Price(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Order_Sector(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name