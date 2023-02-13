from django.db import models


class SexPet(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOT = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=SexPet.choices, default=SexPet.NOT)
    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="pets"
    )
