from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from groups.models import Group
from django.shortcuts import get_object_or_404
from pets.models import Pet
from rest_framework.pagination import PageNumberPagination
from pets.serializers import PetSerializer
from traits.models import Trait


# Create your views here.
class PetsView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        trait = request.query_params.get("trait")

        if trait:
            filter = Pet.objects.filter(traits__name=trait).all()
            result_page = self.paginate_queryset(filter, request)
            serializer = PetSerializer(result_page, many=True)
            return self.get_paginated_response(serializer.data)

        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trait_list = serializer.validated_data.pop("traits")

        groups_data = serializer.validated_data.pop("group")
        obj = Group.objects.filter(
            scientific_name__iexact=groups_data["scientific_name"]).first()

        if not obj:
            obj = Group.objects.create(**groups_data)

        pets_object = Pet.objects.create(**serializer.validated_data, group=obj)

        for traits in trait_list:
            traits_object = Trait.objects.filter(name__iexact=traits["name"]).first()

            if not traits_object:
                traits_object = Trait.objects.create(**traits)
                pets_object.traits.add(traits_object)

            pets_object.traits.add(traits_object)

        serializer = PetSerializer(pets_object)

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetsDetailView(APIView):
    def get(self, request: Request, pet_id) -> Response:
        pets = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pets)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id) -> Response:
        pets = get_object_or_404(Pet, id=pet_id)
        pets.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, pet_id) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        group_dict = serializer.validated_data.pop("group", None)
        traits_list = serializer.validated_data.pop("traits", None)

        if group_dict:
            try:
                groups_updated = Group.objects.get(
                    scientific_name__iexact=group_dict["scientific_name"]
                )
                pet.group = groups_updated

            except Group.DoesNotExist:
                groups_updated = Group.objects.create(**group_dict)
            pet.group = groups_updated

        if traits_list:
            try:
                for traits in traits_list:

                    traits_object = Trait.objects.get(name__iexact=traits["name"])
                    pet.traits.add(traits_object)

            except Trait.DoesNotExist:
                for traits in traits_list:
                    trait_objects = Trait.objects.create(**traits)
                    pet.traits.add(trait_objects)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)
