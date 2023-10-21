from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Einzelteil
from .serializers import EinzelteilSerializer
from .models import Legoset
from .serializers import LegosetSerializer
from .models import Setmarktpreis
from .serializers import SetmarktpreisSerializer
from .models import Einzelteilmarktpreis
from .serializers import EinzelteilmarktpreisSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])
def eingabe_mit_id(request, id):
    try:
        set = Legoset.objects.get(set_id=id)
    except Legoset.DoesNotExist:
        return JsonResponse({'message': 'Die eingegebene ID entspricht keinem Legoset in unserer Datenbank'}, status=status.HTTP_404_NOT_FOUND)
    set_serializer = LegosetSerializer(set)
    return JsonResponse(set_serializer.data)


@api_view(['GET'])
def eingabe_mit_name(request, name):
    try:
        set = Legoset.objects.get(name=name)
    except Legoset.DoesNotExist:
        return JsonResponse({'message': 'Der eingegebene Name entspricht keinem Legoset in unserer Datenbank'}, status=status.HTTP_404_NOT_FOUND)
    set_serializer = LegosetSerializer(set)
    return JsonResponse(set_serializer.data)