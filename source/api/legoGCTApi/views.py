from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.db import connection
from .models import Legoset
from .serializers import LegosetSerializer
from .models import Einzelteil
from .serializers import EinzelteilSerializer
from .models import EinzelteilLegoset
from .serializers import EinzelteilLegosetSerializer
from .models import Setmarktpreis
from .serializers import SetmarktpreisSerializer
from .models import Einzelteilmarktpreis
from .serializers import EinzelteilmarktpreisSerializer
from collections import namedtuple

def result(set):
    result_dict = {}
    with connection.cursor() as cursor:
        def structured_fetchall(cursor):
            result = [set]
            for row in cursor.fetchall():
                entry = list(filter(lambda a: a["einzelteil_id"] == row[0], result[1:]))
                if len(entry) > 0:
                    preis_dict = {"preis": row[3], "anbieter_url": row[2], "url": row[4]}
                    entry[0]["preise"].append(preis_dict)
                else:
                    preis_dict = None
                    if row[3] is not None:
                        preis_dict = [{"preis": row[3], "anbieter_url": row[2], "url": row[4]}]
                    entry = {"einzelteil_id": row[0], "anzahl": row[1], "preise": preis_dict}
                    result.append(entry)
            return result

        cursor.execute('SELECT EL.einzelteil_id, anzahl, anbieter_url, preis, url '
                       'FROM public."Einzelteil_legoset" El LEFT OUTER JOIN "EinzelteilMarktpreis" on '
                       '"EinzelteilMarktpreis".einzelteil_id = El.einzelteil_id WHERE EL.set_id = %s'
                       'GROUP BY EL.einzelteil_id, anzahl, anbieter_url, preis, url', [set["set_id"]])
        result_dict = structured_fetchall(cursor)
        return result_dict

@api_view(['GET'])
def eingabe(request):
    id = request.GET.get('id', None)
    if id is not None:
        try:
            set = Legoset.objects.get(set_id=id)
            setpreis = Setmarktpreis.objects.all().filter(set=set.set_id)
            set_dict = {"set_id": set.set_id, "set_name": set.name, "preis": setpreis[0].preis,
                        "anbieter_url": setpreis[0].anbieter_url.url, "set_url": setpreis[0].url}
        except Legoset.DoesNotExist:
            return JsonResponse({'message': 'Die eingegebene ID entspricht keinem Legoset in unserer Datenbank'},
                                status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(result(set_dict), safe=False)
    name = request.GET.get('name', None)
    if name is not None:
        try:
            set = Legoset.objects.get(name=name)
            setpreis = Setmarktpreis.objects.all().filter(set=set.set_id)
            set_dict = {"set_id": set.set_id, "set_name": set.name, "preis": setpreis[0].preis,
                        "anbieter_url": setpreis[0].anbieter_url.url, "set_url": setpreis[0].url}
        except Legoset.DoesNotExist:
            sets = Legoset.objects.all()
            sets = sets.filter(name__icontains=name)
            if not sets:
                return JsonResponse({'message': 'Der eingegebene Name ähnelt keinem Legoset in unserer Datenbank'},
                                    status=status.HTTP_404_NOT_FOUND)
            sets_serializer = LegosetSerializer(sets, many=True)
            return JsonResponse(sets_serializer.data, safe=False)
        return JsonResponse(result(set_dict), safe=False)
    return JsonResponse({'message': 'Es wurde keine Eingabe getätigt, bitte geben Sie entweder eine ID oder einen '
                                    'Namen in die Suchleiste ein'}, status=status.HTTP_400_BAD_REQUEST)