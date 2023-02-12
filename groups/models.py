from django.db import models


class Group(models.Model):
    scientific_name = models.CharField(max_length=50)
    created_at = models.CharField(max_length=10)
