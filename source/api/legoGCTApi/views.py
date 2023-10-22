from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Legoset
from .serializers import LegosetSerializer
from .models import Einzelteil
from .serializers import EinzelteilSerializer
from .models import Setmarktpreis
from .serializers import SetmarktpreisSerializer
from .models import Einzelteilmarktpreis
from .serializers import EinzelteilmarktpreisSerializer
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
dao = Datenzugriffsobjekt()


@api_view(['GET'])
def eingabe(request):
    id = request.GET.get('id', None)
    if id is not None:
        eingabe_mit_id(request, id)
    name = request.GET.get('name', None)
    if name is not None:
        eingabe_mit_name(request, name)
    return JsonResponse({'message': 'Es wurde keine Eingabe getätigt, bitte geben Sie entweder eine ID oder einen '
                                    'Namen in die Suchleiste ein'}, status=status.HTTP_400_BAD_REQUEST)


def eingabe_mit_id(request, id):
    try:
        set = Legoset.objects.get(set_id=id)
    except Legoset.DoesNotExist:
        return JsonResponse({'message': 'Die eingegebene ID entspricht keinem Legoset in unserer Datenbank'},
                            status=status.HTTP_404_NOT_FOUND)
    set_serializer = LegosetSerializer(set)
    return JsonResponse(set_serializer.data)


def eingabe_mit_name(request, name):
    try:
        set = Legoset.objects.get(name=name)
    except Legoset.DoesNotExist:
        sets = dao.legosets_zu_name(name)
        if not sets:
            return JsonResponse({'message': 'Der eingegebene Name ähnelt keinem Legoset in unserer Datenbank'},
                                status=status.HTTP_404_NOT_FOUND)
        sets_serializer = LegosetSerializer(sets, many=True)
        return JsonResponse(sets_serializer.data, safe=False)
        pass
    set_serializer = LegosetSerializer(set)
    return JsonResponse(set_serializer.data)

