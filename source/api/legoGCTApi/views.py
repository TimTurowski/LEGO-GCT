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


@api_view(['GET'])
def eingabe(request):
    id = request.GET.get('id', None)
    if id is not None:
        try:
            set = Legoset.objects.get(set_id=id)
        except Legoset.DoesNotExist:
            return JsonResponse({'message': 'Die eingegebene ID entspricht keinem Legoset in unserer Datenbank'},
                                status=status.HTTP_404_NOT_FOUND)
        set_serializer = LegosetSerializer(set)
        return JsonResponse(set_serializer.data)
    name = request.GET.get('name', None)
    if name is not None:
        try:
            set = Legoset.objects.get(name=name)
        except Legoset.DoesNotExist:
            sets = Legoset.objects.all()
            sets = sets.filter(name__icontains=name)
            if not sets:
                return JsonResponse({'message': 'Der eingegebene Name ähnelt keinem Legoset in unserer Datenbank'},
                                    status=status.HTTP_404_NOT_FOUND)
            sets_serializer = LegosetSerializer(sets, many=True)
            return JsonResponse(sets_serializer.data, safe=False)
        set_serializer = LegosetSerializer(set)
        return JsonResponse(set_serializer.data)
    return JsonResponse({'message': 'Es wurde keine Eingabe getätigt, bitte geben Sie entweder eine ID oder einen '
                                    'Namen in die Suchleiste ein'}, status=status.HTTP_400_BAD_REQUEST)