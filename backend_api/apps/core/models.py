from django.db import models


class CreatedUpdateBase(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
