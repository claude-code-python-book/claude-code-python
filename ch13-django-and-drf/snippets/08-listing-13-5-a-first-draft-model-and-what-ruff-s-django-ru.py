from django.db import models


class Room(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100, unique=True)
    notes = models.TextField(null=True, blank=True)
    capacity = models.PositiveSmallIntegerField()
