import json

import django.db.utils
import psycopg2.errors
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from django.db import connection
from .models import Legoset, Setmarktpreis, UserSuchliste
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from itertools import groupby


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
        def fetch_shop_results(cursor):

            #Dictonaries für die Verschiedenen Einzelteilanbieter
            lego_dict = {"shop_name": "Lego", "shop_url": "https://www.lego.com/de-de/pick-and-build/pick-a-brick",
                         "parts": []}
            toypro_dict = {"shop_name": "Toypro", "shop_url": "https://www.toypro.com", "parts": []}
            bricklink_dict = {"shop_name": "Bricklink(Lucky-Bricks)",
                              "shop_url": "https://store.bricklink.com/anguray#/shop?o={%22itemType%22:%22P%22,%22catID%22:%2293%22,%22invNew%22:%22N%22,%22showHomeItems%22:0}",
                              "parts": []}
            result_list_shop_structure = [set]

            # erstellt ein dict aus der SQL Querry die id ist der key
            grouped_querry = {key: list(group) for key, group in groupby(cursor.fetchall(), key=lambda x: x[0])}

            for key in grouped_querry.keys():
                einzelteil_dict = grouped_querry[key]

                # tupel nach Shop gruppieren
                row_dict = {key: list(group) for key, group in groupby(einzelteil_dict, key=lambda x: x[2])}
                first_row = list(row_dict.values())[0]

                if "https://www.lego.com/de-de/pick-and-build/pick-a-brick" in row_dict:

                    # erstellen eines Dicts für die Informationen eines Einzelteils für Lego
                    row = row_dict["https://www.lego.com/de-de/pick-and-build/pick-a-brick"][0]
                    part = {"einzelteil_id": row[0], "anzahl": row[1], "preis": float(row[3]), "url": row[2]
                        , "beschreibung": row[5], "kategorie": row[7], "farbe":row[6]}
                    lego_dict["parts"].append(part)
                else:

                    # erstellen eines Dicts für die Informationen eines Einzelteils für Lego
                    # wenn keine Preise bei Lego gefunden worden sind

                    row = first_row[0]
                    part = {"einzelteil_id": row[0], "anzahl": row[1], "preis": None, "url": None
                        , "beschreibung": row[5], "kategorie": row[7], "farbe": row[6]}

                    lego_dict["parts"].append(part)

                if "https://www.toypro.com" in row_dict:

                    # erstellen eines Dicts für die Informationen eines Einzelteils für Toypro

                    row = row_dict["https://www.toypro.com"][0]
                    part = {"einzelteil_id": row[0], "anzahl": row[1], "preis": float(row[3]), "url": row[2]
                        , "beschreibung": row[5], "kategorie": row[7], "farbe": row[6]}

                    toypro_dict["parts"].append(part)
                else:

                    # erstellen eines Dicts für die Informationen eines Einzelteils für Toypro
                    # wenn keine Preise bei Lego gefunden worden sind
                    row = first_row[0]

                    part = {"einzelteil_id": row[0], "anzahl": row[1], "preis": None, "url": None
                        , "beschreibung": row[5], "kategorie": row[7], "farbe": row[6]}

                    toypro_dict["parts"].append(part)

                if "https://store.bricklink.com/anguray#/shop?o={%22itemType%22:%22P%22,%22catID%22:%2293%22,%22invNew%22:%22N%22,%22showHomeItems%22:0}" in row_dict:

                    # erstellen eines Dicts für die Informationen eines Einzelteils für Bricklink

                    row = row_dict["https://store.bricklink.com/anguray#/shop?o={%22itemType%22:%22P%22,%22catID%22:%2293%22,%22invNew%22:%22N%22,%22showHomeItems%22:0}"][0]
                    part = {"einzelteil_id": row[0], "anzahl": row[1], "preis": row[3], "url": row[2]
                        , "beschreibung": row[5], "kategorie": row[7], "farbe": row[6]}

                    bricklink_dict["parts"].append(part)
                else:
                    # erstellen eines Dicts für die Informationen eines Einzelteils für Bricklink
                    # wenn keine Preise bei Lego gefunden worden sind
                    row = first_row[0]
                    part = {"einzelteil_id": row[0], "anzahl": row[1], "preis": None, "url": None
                        , "beschreibung": row[5], "kategorie": row[7], "farbe": row[6]}

                    bricklink_dict["parts"].append(part)

            # zusammenfügen von allen erstellten dict
            result_list_shop_structure.append(lego_dict)
            result_list_shop_structure.append(toypro_dict)
            result_list_shop_structure.append(bricklink_dict)

            return result_list_shop_structure

        # SQL abfrage, wo alle wichtigen Daten fürs Frontend geholt wird
        cursor.execute(
            'SELECT EL.einzelteil_id, anzahl, anbieter_url, preis, url, Ed.beschreibung,Ed.farbe,Ed.kategorie_id'
            ' FROM ("Einzelteil_legoset" El LEFT OUTER JOIN "EinzelteilMarktpreis" on'
            '"EinzelteilMarktpreis".einzelteil_id = El.einzelteil_id) LEFT OUTER JOIN "Einzelteildetails" Ed ON (El.einzelteil_id = Ed.sonderteil_id)'
            'WHERE EL.set_id = %s'
            'GROUP BY EL.einzelteil_id, anzahl, anbieter_url, preis, url, Ed.beschreibung,Ed.farbe,Ed.kategorie_id',
            [set["set_id"]])
        result_dict = fetch_shop_results(cursor)

        # SQL abfrage, wo das Bild zu dem Set geholt wird
        cursor.execute('SELECT set_bild FROM "SetBild" WHERE set = %s', [set["set_id"]])
        result = cursor.fetchall()
        if result:
            set_bild = {"set_bild": result[0]}
        else:
            set_bild = " "

        result_dict.append(set_bild)
        return result_dict


def sets_result(legosets):
    """
    Diese Funktion dient als Hilfsfunktion und macht aus allen übergebenen Legosets ein Dictionary mit den wichtigen
    Informationen
    :param legosets: eine Liste mit den vorgeschlagenen Legosets bei uneindeutiger Namen-Suche
    """
    # Eine Liste für die resultierenden Legoset-Dictionaries erstellen
    legosets_dict = []
    # Durch jedes Legoset in der übergebenen Liste iterieren
    for legoset in legosets:
        # Ein Dictionary für jedes Legoset erstellen und 'set_id' sowie 'set_name' hinzufügen
        result_dict = {"set_id": legoset.set_id, "set_name": legoset.name, "set_bild": ""}
        legosets_dict.append(result_dict)
    return legosets_dict


def verlauf_result(user_id):
    """
    Diese Funktion dient als Hilfsfunktion und gibt zur User-ID die jeweiligen benötigten Daten zurück, für die
    User-Suchliste
    :param user_id: ID des Users
    """
    # Suchverlaufinformationen aus der Datenbank abrufen, beinhaltend Legoset-ID, Legoset-Name, User-Suchliste-ID und
    # Datum der Suche
    with connection.cursor() as cursor:
        cursor.execute('SELECT "Legoset".set_id, name,"UserSuchliste".id, datum '
                       'FROM "UserSuchliste" join "Legoset" on ("Legoset".set_id = "UserSuchliste".set_id) '
                       'WHERE "user" = %s '
                       'ORDER BY datum DESC', [user_id])

        # Ergebnisse in ein Listendictionary umwandeln
        result = []
        for i in cursor.fetchall():
            dict = {"set_id": i[0], "set_name": i[1], "such_id": i[2], "date": i[3]}
            result.append(dict)
    return result


@api_view(['GET'])
def eingabe(request):
    """
    Diese Funktion dient zur Abarbeitung einer HTTP-Request in der Suchleiste und unterscheidet zwischen einer Namen-
    suche, einer ID-Suche und einer Suche wo es einen uneindeutigen Namen gibt
    :param request: komplette HTTP-Request mit allen wichtigen Daten
    """
    # Holen der Parametern 'id' und 'name' aus der GET-Anfrage, falls eine 'id' vorhanden ist, ist es eine ID-Suche und
    # falls ein 'name' vorhanden ist, dann ist es entweder eine eindeutige oder uneindeutige Namensuche
    id = request.GET.get('id', None)

    # track_search bestimmt, ob die Suche in der Datenbank gespeichert wird
    track_search = True

    # wenn die Id mit dem char 't' endet wird die Suche nicht getrackt
    if id is not None and id[-1] == 't':
        id = id[:-1]
        track_search = False

    name = request.GET.get('name', None)

    # Überprüfen, ob ein Authorization-Token in der Anfrage vorhanden ist
    if request.META.get('HTTP_AUTHORIZATION'):
        # Wenn ein Token vorhanden ist, den zugehörigen Benutzer erhalten
        user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION')).user
        # Wenn eine ID-Suche ausgeführt wurde, ein Legoset mit dieser 'id' zur User-Suchliste hinzuzufügen
        if id is not None:
            try:
                set = Legoset.objects.get(set_id=id)
                u = UserSuchliste(set=set, user=user)
                u.save(force_insert=True)
            except Legoset.DoesNotExist:
                pass
        # Wenn ein 'name' vorhanden ist, versuchen, ein Legoset zum eindeutigen oder uneindeutigen Namen zu finden,
        # falls es ein eindeutiger Name ist, wird das Legoset der User-Suchliste hinzugefügt
        if name is not None:
            try:
                set = Legoset.objects.get(name=name)
                u = UserSuchliste(set=set, user=user)
                u.save(force_insert=True)
            except (Legoset.DoesNotExist, Legoset.MultipleObjectsReturned):
                pass

    # Wenn eine ID-Suche ausgeführt wurde, versuchen, Informationen über das Legoset mit dieser 'id' abzurufen
    if id is not None:
        try:
            set = Legoset.objects.get(set_id=id)
            setpreis = Setmarktpreis.objects.all().filter(set=set.set_id)
            if len(setpreis) == 0:
                set_dict = {"set_id": set.set_id, "set_name": set.name, "preis": None,
                            "anbieter_url": None, "set_url": None}
            else:
                set_dict = {"set_id": set.set_id, "set_name": set.name, "preis": setpreis[0].preis,
                            "anbieter_url": setpreis[0].anbieter_url.url, "set_url": setpreis[0].url}
        except Legoset.DoesNotExist:
            return JsonResponse({'message': 'Die eingegebene ID entspricht keinem Legoset in unserer Datenbank'}, safe=False)
        return JsonResponse(result(set_dict), safe=False)

    # Wenn ein 'name' vorhanden ist, versuchen, Informationen über das Legoset mit diesem 'name' abzurufen
    if name is not None:
        try:
            set = Legoset.objects.get(name=name)
            setpreis = Setmarktpreis.objects.filter(set=set.set_id)
            set_dict = {"set_id": set.set_id, "set_name": set.name, "preis": setpreis[0].preis,
                        "anbieter_url": setpreis[0].anbieter_url.url, "set_url": setpreis[0].url}
        # Wenn mehrere Legosets mit dem uneindeutigen Namen in ihrem Namen gefunden wurden, gib die ersten 50 zurück
        except (Legoset.DoesNotExist, Legoset.MultipleObjectsReturned):
            sets = Legoset.objects.filter(name__icontains=name)[:25]

            return JsonResponse(sets_result(sets), safe=False)
        return JsonResponse(result(set_dict), safe=False)
    # Wenn weder 'id' noch 'name' vorhanden sind, gibt einen Fehler zurück
    return JsonResponse({'message': 'Es wurde keine Eingabe getätigt, bitte geben Sie entweder eine ID oder einen '
                                    'Namen in die Suchleiste ein'}, safe=False)


@api_view(['GET'])
def verlauf(request):
    """
    Diese Funktion gibt die Daten für den User-Suchverlauf zurück und nutzt die Hilfsfunktion verlauf_result, um alle
    wichtigen Daten zu erhalten.
    :param request: komplette HTTP-Request mit allen wichtigen Daten
    """
    # Den Benutzer anhand des Authorization-Tokens erhalten
    user = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION')).user.id
    # Rückgabe der Ergebnisse der 'verlauf_result' Methode als JSON
    return JsonResponse(verlauf_result(user), safe=False)


@api_view(['GET'])
def delete_set_entry(request):
    """
    Diese Funktion löscht einen Eintrag von einem User aus seinem Suchverlauf
    :param request: komplette HTTP-Request mit allen wichtigen Daten
    """
    # id die des zu löschenden Eintrags
    id = request.GET.get('id', None)
    # Löschen des Eintrags aus der "UserSuchliste" Tabelle mit der gegebenen ID
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM "UserSuchliste"'
                       'WHERE "UserSuchliste".id = %s', [id])
    return JsonResponse({}, safe=False)


@api_view(['GET'])
def bilder_wiedergabe(request):
    """
    Diese Funktion sucht zu einer Legoset-ID, das jeweilige Bild und sendet dieses zurück
    :param request: komplette HTTP-Request mit allen wichtigen Daten
    """
    # ID aus der GET-Anfrage erhalten
    id = request.GET.get('id', None)
    # Bild zu dem Legoset aus der Datenbank holen
    with connection.cursor() as cursor:
        cursor.execute('SELECT set_bild FROM "SetBild"'
                       'WHERE set = %s', [id])
        result = cursor.fetchall()
        # Überprüfen, ob ein Bild vorhanden ist
        if result:
            set_bild = result[0]
        else:
            set_bild = " "
        result_dict = {"set_bild": set_bild}
    return JsonResponse(result_dict)


@api_view(['POST'])
def register(request):
    """
    Diese Funktion fügt einen neuen Nutzer in unsere Datenbank mit dem gegebenen Passwort und Username
    :param request: komplette HTTP-Request mit allen wichtigen Daten
    """
    # JSON-Daten aus der Anfrage laden
    json_data = json.loads(request.body)
    passwort = json_data['password']
    user = json_data['username']
    # Neuen Benutzer erstellen und speichern
    try:
        u = User.objects.create_user(user, password=passwort)
        u.save()
        return JsonResponse({"user": user})
    except django.db.utils.IntegrityError as error:
        print(error)
        return JsonResponse({"message": "Nutzername bereits vergeben"})

