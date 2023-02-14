from rest_framework import serializers
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    weight = serializers.FloatField(required=True)
    sex = serializers.CharField()
    group = GroupSerializer(required=True)
    traits = TraitSerializer(many=True, required=True)
