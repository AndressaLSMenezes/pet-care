from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from pets.serializers import PetSerializer
from .models import Pet
from groups.models import Group
from traits.models import Trait


class PetView(APIView, PageNumberPagination):
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            group_data = serializer.validated_data.pop("group")
            scientific_name = group_data.get("scientific_name").lower()
            group, created = Group.objects.get_or_create(
                scientific_name=scientific_name,
                defaults={"scientific_name": scientific_name},
            )

            trait_data = serializer.validated_data.pop("traits")
            trait_names = [trait.get("name").lower() for trait in trait_data]
            new_traits = []
            for trait_name in trait_names:
                trait, created = Trait.objects.get_or_create(
                    name=trait_name, defaults={"name": trait_name}
                )
                new_traits.append(trait)

            pet = Pet.objects.create(group=group, **serializer.validated_data)
            pet.traits.set(new_traits)
            return Response(PetSerializer(pet).data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class PetDetailView(APIView):
    def get(self, request, pet_id):
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def delete(self, request, pet_id):
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        pet.delete()
        return Response(status=204)

    def patch(self, request, pet_id):
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)


class PetFindView(APIView):
    def get(self, request):
        trait = request.query_params.get("trait", None)
        pets = Pet.objects.filter(traits__contains=trait)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
