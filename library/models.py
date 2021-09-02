from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    code = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
