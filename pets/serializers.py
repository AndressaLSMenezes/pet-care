from rest_framework import serializers
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer
from .models import SexPet


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SexPet.choices, default=SexPet.DEFAULT)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
