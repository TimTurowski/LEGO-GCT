from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, distinct
from sqlalchemy import func
import os

if(os.name == 'posix'):
    from DiscordBot.dc_message import send_discord_message
    from Entity import entities
else:
    from source.DiscordBot.dc_message import send_discord_message
    from source.Entity import entities


class Datenzugriffsobjekt:

    def __init__(self):
        engine = create_engine("postgresql+psycopg2://postgres:27R569RX@192.168.198.47:5432/LegoGCT")
        self.Session = sessionmaker(engine)

    def einzelteil_liste(self):
        """
        Diese Funktion liefert eine Liste von allen Einzelteilen in der Datenbank
        """
        session = self.Session()
        result = session.query(entities.Einzelteil).all()
        return result

    def einzelteildetail_liste(self):
        """
        Diese Funktion liefert eine Liste von allen Einzelteildetails
        """
        session = self.Session()
        result = session.query(entities.Einzelteildetails).all()
        return result

    def lego_set_liste(self):
        """
        Diese Funktion liefert eine Liste von allen Legosets in der Datenbank
        """
        session = self.Session()
        result = session.query(entities.Legoset).all()
        return result

    def loesche_sets(self, sets):
        """
        Diese Funktion setzt das entfernen von Sets aus der Datenbank um
        :param sets: eine Liste von Legosets
        :type: Liste mit Legosets
        """
        with self.Session() as session:
            with session.begin():
                for i in sets:
                    session.delete(i)
                session.commit()
            session.close()

    def einzelteil_ohne_marktpreis(self, anbieter):
        """
        Diese Funktion liefert eine Liste von Einzelteilen eines angegebenen
        Anbieters, welche noch keinen Marktpreis besitzen
        :param anbieter: Anbieter, nach dem gefiltert wird
        :type anbieter: String
        """
        session = self.Session()
        all_parts = session.query(entities.Einzelteil.einzelteil_id).all()
        print(all_parts)
        result = session.query(entities.EinzelteilMarktpreis.einzelteil_id) \
            .filter(entities.EinzelteilMarktpreis.anbieter_url == anbieter).all()
        return list(set(all_parts) - set(result))

    def einzelteile_zu_legoset(self, set_id):
        """
        Diese Funktion liefert eine Liste von allen Einzelteilen eines angegebenen Legosets
        :param set_id: eine SetID nach der die Einzelteile gesucht werden
        :type set_id: string
        """
        session = self.Session()
        result = session.query(entities.Einzelteil).join(entities.Einzelteil.sets).filter(entities.EinzelteilLegoset.set_id == set_id)
        return result

    def legosets_zu_name(self, name):
        """
        Diese Funktion liefert alle LegosetIDs, in welchem der angegebene Name enthalten ist
        :param name: ein Name, zu dem die LegosetId(s) gesucht werden
        :type name: string
        """
        session = self.Session()
        result = session.query(entities.Legoset).filter(entities.Legoset.name.like("%{}%".format(name))).all()
        return result

    def fuge_set_bild_hinzu(self, id, bild):
        """
        Diese Funktion fügt einem vorhandenen Legoset ein Bild hinzu
        :param id: LegosetID, welchem ein Bild hinzugefügt werden soll
        :type id: string
        :param bild: das Bild, welches hinzugefügt wird
        :type bild: string
        """
        session = self.Session()
        set_bild = entities.SetBild(set=id,set_bild=bild)
        session.merge(set_bild)
        session.commit()
        session.close()

    def fuge_kategorie_hinzu(self, kategorie):
        """
        Diese Funktion fügt eine neue Kategorie in die Datenbank ein
        :param kategorie: eine Kategorie zur Kategorisierung von Einzelteilen
        :type kategorie: entities.Kategorie
        """
        session = self.Session()
        session.merge(kategorie)
        session.commit()
        session.close()

    def lego_set_mit_einzelteil_ohne_einzelteildetails(self, zahl):

        session = self.Session()
        result = (session.query(entities.Legoset.set_id,func.count(distinct(entities.Einzelteil.einzelteil_id)))
                  .join(entities.EinzelteilLegoset, entities.Legoset.set_id == entities.EinzelteilLegoset.set_id)
                  .join(entities.Einzelteil, entities.EinzelteilLegoset.einzelteil_id ==
                        entities.Einzelteil.einzelteil_id)
                  .outerjoin(entities.Einzelteildetails, entities.Einzelteil.einzelteil_id ==
                             entities.Einzelteildetails.sonderteil_id)
                  .filter(entities.Einzelteildetails.sonderteil_id.is_(None))
                  .group_by(entities.Legoset.set_id)
                  .having(func.count(distinct(entities.Einzelteil.einzelteil_id)) > zahl).all())
        return result

    def lego_set_liste_ohne_bilder(self):
        """
        Methode um alle Legosets auszugeben, die kein Bild haben
        """
        session = self.Session()
        # Unterabfrage wo alle SetBilder abgefragt werden
        subquery = session.query(entities.SetBild.set)
        result = session.query(entities.Legoset).filter(entities.Legoset.set_id.not_in(subquery))
        return result

    def einzelteil_marktpreis_liste(self, anbieter):
        """
        Methode um eine Liste von Marktpreisen zu einem Anbieter auszugeben
        :param anbieter: ein Anbieter, von dem die Marktpreiseliste erstellt werden soll
        :type anbieter: entities.Anbieter
        """
        session = self.Session()
        result = session.query(entities.EinzelteilMarktpreis.einzelteil_id)\
            .filter(entities.EinzelteilMarktpreis.anbieter_url == anbieter).all()
        return result

    def update_einzelteil_marktpreise(self, new_marktpreise):
        """
        Methode um eine Liste von Marktpreisen zu aktualisieren und Benachrichtigung auf discord von den neuen
        Einzeilteilmarktpreise
        :param new_marktpreise: eine Liste mit allen neuen Marktpreise die hinzugefügt werden sollen
        :type new_marktpreise: Liste von entities.EinzelteilMarktpreis
        """
        session = self.Session()
        update_count = 0

        for i in new_marktpreise:

            # aktuelles Preis Objekt von der Datenbank holen
            marktpreis_entity = session.query(entities.EinzelteilMarktpreis)\
                .filter(entities.EinzelteilMarktpreis.einzelteil_id == i.einzelteile.einzelteil_id)\
                .filter(entities.EinzelteilMarktpreis.anbieter_url == i.anbieter.url).first()
            if marktpreis_entity is None:
                session.merge(i)
                update_count += 1
            else:
                # Preis aktualisieren und mitzählen für die Discord Ausgabe
                if float(marktpreis_entity.preis) != float(i.preis):
                    update_count += 1
                    marktpreis_entity.preis = i.preis
        send_discord_message(f"```ansi\n[0;36m{update_count} Einzelteile von {len(new_marktpreise)}"
                             f" haben einen neuen Preis```")
        session.commit()

    def remove_einzelteil_marktpreise(self, einzelteile, shop_url):
        """
        Methode zum entfernen EinzelteilMarktpreise
        :param einzelteile: Die Einzelteile, von dem der Marktpreis entfernt werden soll
        :type einzelteile: Liste von entities.Einzelteil
        :param shop_url: die URL zum Anbieter, von welchem der Marktpreis nicht mehr vorhanden ist
        :type shop_url: string
        """
        session = self.Session()
        for i in einzelteile:
            # Sucht das Marktpreisobjekt zur Einzelteil-ID
            marktpreis_entity = session.query(entities.EinzelteilMarktpreis)\
                .filter(entities.EinzelteilMarktpreis.einzelteile == i)\
                .filter(entities.EinzelteilMarktpreis.anbieter_url == shop_url).first()
            print(marktpreis_entity)
            # Löscht das Markpreis Objekt
            if marktpreis_entity is not None:
                session.delete(marktpreis_entity)
        session.commit()

    def anbieter_liste(self):
        """
        Diese Funktion liefert eine Liste von allen Anbietern
        """
        session = self.Session()
        result = session.query(entities.Anbieter).all()
        return result

    def fuge_einzelteildetails_hinzu(self, einzelteildetails):
        """
        Diese Funktion fügt in die Datenbank neue Einzelteildetail Objekte hinzu
        :param einzelteildetails: Einzelteildetail Objekte welche hinzugefügt werden sollen
        :type einzelteildetails: Liste von entities.Einzelteildetails
        """
        with self.Session() as session:
            with session.begin():
                for i in einzelteildetails:
                    result = "Das übergebene Objekt ist kein Einzelteildetails"
                    # Überprüfung, ob das übergebene Objekt überhaupt ein Einzelteildetail ist
                    if isinstance(i, entities.Einzelteildetails):
                        # Hier wird kontrolliert, ob der Fremdschlüssel von Einzelteildetails schon in der
                        # Datenbank vorhanden ist
                        if not session.query(i.__class__) \
                                .filter(entities.Einzelteildetails.sonderteil_id == i.einzelteile.einzelteil_id).all():
                            session.merge(i)
                            result = "Neues Einzelteildetails wurde hinzugefügt"
                        else:
                            result = "Einzelteildetails ist schon vorhanden"
                    # Falls man im Python prompt sehen will, ob irgendwas hinzugefügt wird oder vorhand ist, die nächste
                    # Zeile auskommentieren
                    # print(result)
                session.commit()
            session.close()

    def fuge_einzelteil_marktpreis_hinzu(self, einzelteil_marktpreis):
        """
        Fügt EinzelteilMarktpreis Objekte der Datenbank hinzu
        :param einzelteil_marktpreis: EinzelteilMarktpreis Objekte, welche hinzugefügt werden sollen
        :type einzelteil_marktpreis: Liste von entities.EinzelteilMarktpreis
        """
        with self.Session() as session:
            with session.begin():
                for i in einzelteil_marktpreis:
                    result = "Das übergebene Objekt ist kein EinzelteilMarktpreis"
                    # Überprüfung ob das übergebene Objekt überhaupt ein Einzelteilmarktpreis ist
                    if isinstance(i, entities.EinzelteilMarktpreis):
                        # Hier wird kontrolliert, ob der zusammengesetzter Schlüssel vom EinzelteilMarktpreis schon in
                        # der Datenbank vorhanden ist
                        if not session.query(i.__class__) \
                                .filter(
                            entities.EinzelteilMarktpreis.einzelteil_id == i.einzelteile.einzelteil_id) \
                                .filter(
                                entities.EinzelteilMarktpreis.anbieter_url == i.anbieter.url).all():
                            session.merge(i)
                            result = "Neues EinzelteilMarktpreis wurde hinzugefügt"
                        else:
                            result = "EinzelteilMarktpreis ist schon vorhanden"
                    # Falls man im Python prompt sehen will, ob irgendwas hinzugefügt wird oder vorhand ist, die nächste
                    # Zeile auskommentieren
                    # print(result)
                session.commit()
            session.close()

    def fuge_set_marktpreis_hinzu(self, set_marktpreis):
        """
        Diese Funktion erweitert die Datenbank um SetMarktpreise
        :param set_marktpreis: Setmarktpreis Objekte, welche hinzugefügt werden sollen
        :type set_marktpreis: Liste von entities.SetMarktpreis
        """
        with self.Session() as session:
            with session.begin():
                for i in set_marktpreis:
                    result = "Das übergebene Objekt ist kein SetMarktpreis"
                    # Überprüfung ob das übergebene Objekt überhaupt ein SetMarktpreis ist
                    if isinstance(i, entities.SetMarktpreis):
                        # Hier wird kontrolliert, ob der zusammengesetzter Schlüssel vom SetMarktpreis schon in der
                        # Datenbank vorhanden ist
                        set_preis = session.query(i.__class__).filter(entities.SetMarktpreis.set_id == i.set.set_id) \
                                .filter(entities.SetMarktpreis.anbieter_url == i.anbieter.url).first()
                        if not set_preis:
                            session.merge(i)
                            result = "Neues SetMarktpreis wurde hinzugefügt"
                        else:
                            if float(set_preis.preis) != float(i.preis):
                                set_preis.preis = i.preis
                                result = "SetMarktpreis ist schon vorhanden und Preis wurde geändert"
                            else:
                                result = "SetMarktpreis ist schon vorhanden und Preis ist gleich geblieben"
                    # Falls man im Python prompt sehen will, ob irgendwas hinzugefügt wird oder vorhand ist, die nächste
                    # Zeile auskommentieren
                    # print(result)
                session.commit()
            session.close()


    def fuge_einzelteil_legoset_hinzu(self, einzelteil_legoset):
        """
        Diese Funktion fügt der Datenbank EinzelteilLegosets hinzu
        :param einzelteil_legoset: EinzelteilLegosets, welche hinzugefügt werden sollen
        :type einzelteil_legoset: Liste von entities.EinzelteilLegoset
        """
        with self.Session() as session:
            with session.begin():
                for i in einzelteil_legoset:
                    result = "Das übergebene Objekt ist kein EinzelteilLegoset"
                    # Überprüfung ob das übergebene Objekt überhaupt ein EinzelteilLegoset ist
                    try:
                        if isinstance(i, entities.EinzelteilLegoset):
                            # Hier wird kontrolliert, ob der zusammengesetzter Schlüssel vom EinzelteilLegoset schon
                            # in der Datenbank vorhanden ist
                            if not session.query(i.__class__) \
                                    .filter(
                                entities.EinzelteilLegoset.einzelteil_id == i.einzelteile.einzelteil_id) \
                                    .filter(entities.EinzelteilLegoset.set_id == i.set.set_id).all():
                                session.merge(i)
                                result = "Neues EinzelteilLegoset wurde hinzugefügt"
                            else:
                                result = "EinzelteilLegoset ist schon vorhanden"
                    except Exception as e:
                        pass
                    # Falls man im Python prompt sehen will, ob irgendwas hinzugefügt wird oder vorhand ist, die nächste
                    # Zeile auskommentieren
                    # print(result)
                session.commit()
            session.close()


    def fuge_anbieter_hinzu(self, anbieter):
        """
        Diese Funktion fügt einen neuen Anbieter der Datenbank hinzu
        :param anbieter: ein Anbieter Objekt, welches hinzugefügt werden soll
        :type anbieter: Anbieter Objekt
        """
        with self.Session() as session:
            with session.begin():
                result = "Das übergebene Objekt ist kein Anbieter"
                # Überprüfung ob das übergebene Objekt überhaupt ein Anbieter ist
                if isinstance(anbieter, entities.Anbieter):
                    # Hier wird kontrolliert, ob der Anbieter schon in der Datenbank vorhanden ist
                    if not session.query(anbieter.__class__).filter(entities.Anbieter.url == anbieter.url).all():
                        session.merge(anbieter)
                        result = "Neuer Anbieter wurde hinzugefügt"
                    else:
                        result = "Anbieter ist schon vorhanden"
                # Falls man im Python prompt sehen will, ob irgendwas hinzugefügt wird oder vorhand ist, die nächste
                # Zeile auskommentieren
                # print(result)
                session.commit()
            session.close()





