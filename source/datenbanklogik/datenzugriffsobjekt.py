from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
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

    """Eine Liste von allen Einzelteilen wird übergeben"""

    def einzelteil_liste(self):
        session = self.Session()
        result = session.query(entities.Einzelteil).all()
        return result

    """Eine Liste von allen Legosets wird übergeben"""

    def lego_set_liste(self):
        session = self.Session()
        result = session.query(entities.Legoset).all()
        return result

    def lego_set_liste_ohne_bilder(self):
        session = self.Session()
        subquery = session.query(entities.SetBild.set)
        result = session.query(entities.Legoset).filter(entities.Legoset.set_id.not_in(subquery))
        return result

    """Eine Liste von allen Einzelteilpreisen wird ausgegeben"""

    def einzelteil_marktpreis_liste(self, anbieter):
        session = self.Session()
        result = session.query(entities.EinzelteilMarktpreis.einzelteil_id)\
            .filter(entities.EinzelteilMarktpreis.anbieter_url == anbieter).all()
        return result

    def sonderteil_liste(self):
        session = self.Session()
        return session.query(entities.Sonderteile).all()


    def update_einzelteil_marktpreise(self, new_marktpreise):
        """Methode um eine Liste von Marktpreisen zu aktualisieren
        :param new_marktpreise:
        :type new_marktpreise:
        """
        session = self.Session()
        update_count = 0

        for i in new_marktpreise:

            # aktuelles Preis Objekt von der Datenbank holen
            marktpreis_entity = session.query(entities.EinzelteilMarktpreis)\
                .filter(entities.EinzelteilMarktpreis.einzelteil_id == i.einzelteile.einzelteil_id)\
                .filter(entities.EinzelteilMarktpreis.anbieter_url == i.anbieter.url).first()

            # Preis aktualisieren und mitzählen für die Discord Ausgabe
            if float(marktpreis_entity.preis) != float(i.preis):
                update_count += 1
                marktpreis_entity.preis = i.preis
        send_discord_message(f"```ansi\n[0;36m{update_count} Einzelteile von {len(new_marktpreise)} haben einen neuen Preis```")
        session.commit()

    def remove_einzelteil_marktpreise(self, einzelteile, shop_url):
        """
        Methode zum entfernen eines Einzelteil Marktpreises
        :param einzelteile: Das Einzelteil, von dem der Marktpreis entfernt werden soll
        :type einzelteile: Ein Objekt vom Typ Einzelteil
        :param shop_url: die URL zum Anbieter, von welchem der Marktpreis nichtmehr vorhanden ist
        :type shop_url:
        """
        session = self.Session()
        for i in einzelteile:
            # Sucht das Marktpreisobjekt zur Einzelteil-ID
            marktpreis_entity = session.query(entities.EinzelteilMarktpreis)\
                .filter(entities.EinzelteilMarktpreis.einzelteile == i)\
                .filter(entities.EinzelteilMarktpreis.anbieter_url == shop_url).first()
            print(marktpreis_entity)
            # Löscht das Markpreis Objekt
            session.delete(marktpreis_entity)
        session.commit()




    def anbieter_liste(self):
        """Diese Funktion liefert eine Liste von allen Anbietern
        """
        session = self.Session()
        result = session.query(entities.Anbieter).all()
        return result


    def fuge_einzelteil_marktpreis_hinzu(self, einzelteil_marktpreis):
        """
        Fügt ein EinzelteilMarktpreis Objekt der Datenbank hinzu
        :param einzelteil_marktpreis: ein EinzelteilMarktpreis Objekt, welches hinzugefügt werden soll
        :type einzelteil_marktpreis: EinzelteilMarktpreis Objekt
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
                    print(result)
                session.commit()
            session.close()



    def fuge_set_marktpreis_hinzu(self, set_marktpreis):
        """
        Diese Funktion erweitert die Datenbank um ein SetMarktpreis
        :param set_marktpreis: ein Setmarktpreis Objekt, welches hinzugefügt werden soll
        :type set_marktpreis: SetMarktpreis Objekt
        """
        with self.Session() as session:
            with session.begin():
                for i in set_marktpreis:
                    result = "Das übergebene Objekt ist kein SetMarktpreis"
                    # Überprüfung ob das übergebene Objekt überhaupt ein SetMarktpreis ist
                    if isinstance(i, entities.SetMarktpreis):
                        # Hier wird kontrolliert, ob der zusammengesetzter Schlüssel vom SetMarktpreis schon in der
                        # Datenbank vorhanden ist
                        if not session.query(i.__class__) \
                                .filter(entities.SetMarktpreis.set_id == i.set.set_id) \
                                .filter(entities.SetMarktpreis.anbieter_url == i.anbieter.url).all():
                            session.merge(i)
                            result = "Neues SetMarktpreis wurde hinzugefügt"
                        else:
                            result = "SetMarktpreis ist schon vorhanden"
                    print(result)
                session.commit()
            session.close()


    def fuge_einzelteil_legoset_hinzu(self, einzelteil_legoset):
        """
        Diese Funktion fügt der Datenbank ein EinzelteilLegoset hinzu
        :param einzelteil_legoset: ein EinzelteilLegoset, welches hinzugefügt werden soll
        :type einzelteil_legoset: EinzelteilLegoset Objekt
        """
        with self.Session() as session:
            with session.begin():
                for i in einzelteil_legoset:
                    result = "Das übergebene Objekt ist kein EinzelteilLegoset"
                    # Überprüfung ob das übergebene Objekt überhaupt ein EinzelteilLegoset ist
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
                    print(result)
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
                    if not session.query(anbieter.__class__).filter(entities.Anbieter.url == anbieter.url).all():
                        session.merge(anbieter)
                        result = "Neuer Anbieter wurde hinzugefügt"
                    else:
                        result = "Anbieter ist schon vorhanden"
                print(result)
                session.commit()
            session.close()


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

    def marktpreise_zu_einzelteile(self, einzelteilliste):
        session = self.Session()
        result = session.query(entities.EinzelteilMarktpreis).join(entities.EinzelteilMarktpreis.einzelteile).filter(entities.EinzelteilMarktpreis.einzelteil_id == i.einzelteil_id)
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
        :type bild: ?!?!?
        """
        session = self.Session()
        set_bild = entities.SetBild(set=id,set_bild=bild)
        session.merge(set_bild)
        session.commit()
        session.close()

    def fuge_kategorie_hinzu(self, kategorie):
        """
        Diese Funktion fügt eine neue Kategorie in die Datenbank ein
        :param kategorie: ?!?!?
        :type kategorie: ?!?!?
        """
        session = self.Session()
        session.merge(kategorie)
        session.commit()
        session.close()

    def fuge_einzelteildetails_hinzu(self, einzelteildetail):
        """
        Diese Funktion fügt in die Datenbank ein neues Einzelteildetail Objekt ein
        :param einzelteildetail: Einzelteildetail Objekt welches hinzugefügt werden soll
        :type einzelteildetail: EinzelteilDetails Objekt
        """
        with (self.Session() as session):
            with session.begin():
                for i in einzelteildetail:
                    result = "Das übergebene Objekt ist kein Einzelteildetails"
                    if isinstance(i, entities.Einzelteildetails):
                        """Hier wird kontrolliert, ob der Fremdschlüssel von Einzelteildetails schon in der
                                            Datenbank vorhanden ist"""
                        if not session.query(i.__class__) \
                                .filter(entities.Einzelteildetails.sonderteil_id == i.einzelteile.einzelteil_id).all():
                            session.merge(i)
                            result = "Neues Einzelteildetails wurde hinzugefügt"
                        else:
                            result = "Einzelteildetails ist schon vorhanden"
                    # print(result)
                session.commit()
            session.close()


