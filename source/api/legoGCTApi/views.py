from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.db import connection
from .models import Legoset, Setmarktpreis, UserSuchliste
from rest_framework.authtoken.models import Token


def result(set):



    result_dict = {}
    with connection.cursor() as cursor:

        def structured_fetchall(cursor):
            result = []
            for row in cursor.fetchall():
                entry = list(filter(lambda a: a["einzelteil_id"] == row[0], result))
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

        cursor.execute('SELECT set_bild FROM "SetBild" WHERE set = %s', [set["set_id"]])
        result = cursor.fetchall()
        if result:
            set_bild = {"set_bild": result[0]}
        else:
            set_bild = " "
        """ändern der JSON Struktur zur einfacheren interpretation im Frontend"""
        lego_dict = {"shop_name":"Lego", "shop_url":"https://www.lego.com/de-de/pick-and-build/pick-a-brick", "parts":[]}
        toypro_dict = {"shop_name":"Toypro", "shop_url":"https://www.toypro.com", "parts":[]}
        bricklink_dict = {"shop_name":"Bricklink(Lucky-Bricks)", "shop_url":"https://store.bricklink.com/anguray#/shop?o={%22itemType%22:%22P%22,%22catID%22:%2293%22,%22invNew%22:%22N%22,%22showHomeItems%22:0}", "parts":[]}
        result_list_shop_structure = [set]
        for i in result_dict:
            lego_einzelteil = {"einzelteil_id": i["einzelteil_id"], "anzahl":i["anzahl"], "preis":None, "url":None}
            toypro_einzelteil = {"einzelteil_id": i["einzelteil_id"], "anzahl":i["anzahl"], "preis":None, "url":None}
            bricklink_einzelteil = {"einzelteil_id": i["einzelteil_id"], "anzahl":i["anzahl"], "preis":None, "url":None}
            if i["preise"] is not None:
                for j in i["preise"]:
                    if j["anbieter_url"] == "https://www.lego.com/de-de/pick-and-build/pick-a-brick":
                        lego_einzelteil["preis"] = j["preis"]
                        lego_einzelteil["url"] = j["url"]
                    if j["anbieter_url"] == "https://www.toypro.com":
                        toypro_einzelteil["preis"] = j["preis"]
                        toypro_einzelteil["url"] = j["url"]
                    if j["anbieter_url"] == "https://store.bricklink.com/anguray#/shop?o={%22itemType%22:%22P%22,%22catID%22:%2293%22,%22invNew%22:%22N%22,%22showHomeItems%22:0}":
                        bricklink_einzelteil["preis"] = j["preis"]
                        bricklink_einzelteil["url"] = j["url"]
            lego_dict["parts"].append(lego_einzelteil)
            toypro_dict["parts"].append(toypro_einzelteil)
            bricklink_dict["parts"].append(bricklink_einzelteil)
        result_list_shop_structure.append(lego_dict)
        result_list_shop_structure.append(toypro_dict)
        result_list_shop_structure.append(bricklink_dict)
        result_list_shop_structure.append(set_bild)
        return result_list_shop_structure


def sets_result(legosets):
    legosets_dict = []
    with connection.cursor() as cursor:
        for legoset in legosets:
            cursor.execute('SELECT set_bild FROM "SetBild" WHERE set = %s', [legoset.set_id])
            result = cursor.fetchall()
            if result:
                set_bild = result[0]
            else:
                set_bild = " "
            result_dict = {"set_id": legoset.set_id, "set_name": legoset.name, "set_bild": set_bild}
            legosets_dict.append(result_dict)
    return legosets_dict

def verlauf_result(user_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT "Legoset".set_id, name,"UserSuchliste".id, datum '
                       'FROM "UserSuchliste" join "Legoset" on ("Legoset".set_id = "UserSuchliste".set_id) '
                       'WHERE "user" = %s '
                       'ORDER BY datum DESC', [user_id])
        result = []
        for i in cursor.fetchall():
            dict = {"set_id": i[0],"set_name": i[1],"such_id": i[2],"date": i[3]}
            result.append(dict)
    return result


@api_view(['GET'])
def eingabe(request):
    id = request.GET.get('id', None)
    name = request.GET.get('name', None)
    if request.META.get('HTTP_AUTHORIZATION'):
        user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION')).user
        if id is not None:
            try:
                set = Legoset.objects.get(set_id=id)
                u = UserSuchliste(set=set, user=user)
                u.save(force_insert=True)
            except Legoset.DoesNotExist:
                pass
        if name is not None:
            try:
                set = Legoset.objects.get(name=name)
                u = UserSuchliste(set=set, user=user)
                u.save(force_insert=True)
            except (Legoset.DoesNotExist, Legoset.MultipleObjectsReturned):
                pass
    if id is not None:
        try:
            set = Legoset.objects.get(set_id=id)
            setpreis = Setmarktpreis.objects.all().filter(set=set.set_id)
            if len(setpreis) == 0:
                set_dict = {"set_id": set.set_id, "set_name": set.name, "preis": None,
                            "anbieter_url": None, "set_url":None}
            else:
                set_dict = {"set_id": set.set_id, "set_name": set.name, "preis": setpreis[0].preis,
                            "anbieter_url": setpreis[0].anbieter_url.url, "set_url": setpreis[0].url}
        except Legoset.DoesNotExist:
            return JsonResponse({'message': 'Die eingegebene ID entspricht keinem Legoset in unserer Datenbank'},
                                status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(result(set_dict), safe=False)
    if name is not None:
        try:
            set = Legoset.objects.get(name=name)
            setpreis = Setmarktpreis.objects.filter(set=set.set_id)
            set_dict = {"set_id": set.set_id, "set_name": set.name, "preis": setpreis[0].preis,
                        "anbieter_url": setpreis[0].anbieter_url.url, "set_url": setpreis[0].url}
        except (Legoset.DoesNotExist, Legoset.MultipleObjectsReturned):
            sets = Legoset.objects.filter(name__icontains=name)[:5]
            if not sets:
                return JsonResponse({'message': 'Der eingegebene Name ähnelt keinem Legoset in unserer Datenbank'},
                                    status=status.HTTP_404_NOT_FOUND)
            return JsonResponse(sets_result(sets), safe=False)
        return JsonResponse(result(set_dict), safe=False)
    return JsonResponse({'message': 'Es wurde keine Eingabe getätigt, bitte geben Sie entweder eine ID oder einen '
                                    'Namen in die Suchleiste ein'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verlauf(request):
    user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION')).user.id

    return JsonResponse(verlauf_result(user), safe=False)

@api_view(['GET'])
def delete_set_entry(request):
    #id die des zu löschenden Eintrags
    id = request.GET.get('id', None)

    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM "UserSuchliste"'
                     'WHERE "UserSuchliste".id = %s', [id])

    return JsonResponse({}, safe=False)



