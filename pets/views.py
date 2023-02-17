from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from pets.serializers import PetSerializer
from .models import Pet
from groups.models import Group
from traits.models import Trait
from rest_framework import serializers


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
                traits = Trait.objects.filter(name__iexact=trait_name)
                if traits.exists():
                    trait = traits.first()
                else:
                    trait = Trait.objects.create(name=trait_name)
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
    pagination_class = PageNumberPagination
    page_size = 1

    def get(self, request, pet_id):
        try:
            pet = Pet.objects.get(pk=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        trait = request.query_params.get("trait", None)
        if trait:
            pets = Pet.objects.filter(traits__name=trait)
            serializer = PetSerializer(pets, many=True)
            return Response(serializer.data)

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

        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            group_data = serializer.validated_data.pop("group", None)
            if group_data:
                group_obj = Group.objects.filter(scientific_name__iexact=group_data.get("scientific_name"))
                if group_obj.exists():
                    group = group_obj.first()
                else:
                    group = Group.objects.create(scientific_name=group_data.get("scientific_name"))
                pet.group = group

            trait_data = serializer.validated_data.pop("traits", None)
            if trait_data:
                trait_names = [trait.get("name").lower() for trait in trait_data]
                new_traits = []
                for trait_name in trait_names:
                    traits = Trait.objects.filter(name__iexact=trait_name)
                    if traits.exists():
                        trait = traits.first()
                    else:
                        trait = Trait.objects.create(name=trait_name)
                    new_traits.append(trait)
                pet.traits.set(new_traits)
        for key, value in serializer.validated_data.items():
            try:
                if key == "sex":
                    serializer.validate_sex(value)
            except serializers.ValidationError as err:
                return Response({"message": err.message}, status=400)
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)
        return Response(serializer.data)


# class PetFindView(APIView):
#     def get(self, request):
#         trait = request.query_params.get("trait", None)
#         pets = Pet.objects.filter(traits__contains=trait)
#         serializer = PetSerializer(pets, many=True)
#         return Response(serializer.data)
