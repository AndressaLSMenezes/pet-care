from rest_framework import serializers
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer
from .models import SexPet


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField(required=False)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def validate_sex(self, value):
        if value not in dict(SexPet.choices):
            raise serializers.ValidationError("Invalid sex value")
        return value
