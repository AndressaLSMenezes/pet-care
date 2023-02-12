from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from serializers import PetSerializer
from models import Pet


class PetView(APIView, PageNumberPagination):
    def post(self, request):
        """
        Aqui vou ter que criar o Group e as traits, mas caso o usuário tente inserir um dado de pet com grupo ou características que já estão salvas no banco de dados, não deve ser criado novamente o grupo ou a(s) característica(s) e sim devem ser utilizados os registros que já existem.
        """
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        pet = Pet.objects.create(**serializer.validated_data)
        serializer = PetSerializer(pet)

        return Response(serializer.data, 201)

    def get(self, request):
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
