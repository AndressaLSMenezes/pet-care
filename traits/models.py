from django.db import models


# Create your models here.
class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)
    created_at = models.CharField(max_length=10)
    pets = models.ManyToManyField("pets.Pet", related_name="traits")
