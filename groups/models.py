from django.db import models

# Create your models here.


class Group(models.Model):
    scientific_name = models.CharField(max_length=50)
    created_at = models.CharField(max_length=10)
