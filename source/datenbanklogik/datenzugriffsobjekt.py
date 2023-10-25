from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
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

    """Eine Liste von allen Anbietern wird übergeben"""

    def anbieter_liste(self):
        session = self.Session()
        result = session.query(entities.Anbieter).all()
        return result

    """Das übergebene Objekt wird kontrolliert, ob es ein EinzelteilMarktpreis ist und ob der EinzelteilMarktpreis schon
     in der Datenbank vorhanden ist, falls alles passt, dann wird der neue EinzelteilMarktpreis hinzugefügt. Es wird je 
     nach Fall eine dementsprechende Meldung geprintet"""

    def fuge_einzelteil_marktpreis_hinzu(self, einzelteil_marktpreis):
        with self.Session() as session:
            with session.begin():
                for i in einzelteil_marktpreis:
                    result = "Das übergebene Objekt ist kein EinzelteilMarktpreis"
                    if isinstance(i, entities.EinzelteilMarktpreis):
                        """Hier wird kontrolliert, ob der zusammengesetzter Schlüssel vom EinzelteilMarktpreis schon in 
                                            der Datenbank vorhanden ist"""
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

    """Das übergebene Objekt wird kontrolliert, ob es ein SetMarktpreis ist und ob der SetMarktpreis schon in der
     Datenbank vorhanden ist, falls alles passt, dann wird der neue SetMarktpreis hinzugefügt. Es wird je nach Fall eine
     dementsprechende Meldung geprintet"""

    def fuge_set_marktpreis_hinzu(self, set_marktpreis):
        with self.Session() as session:
            with session.begin():
                for i in set_marktpreis:
                    result = "Das übergebene Objekt ist kein SetMarktpreis"
                    if isinstance(i, entities.SetMarktpreis):
                        """Hier wird kontrolliert, ob der zusammengesetzter Schlüssel vom SetMarktpreis schon in der
                                            Datenbank vorhanden ist"""
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

    """Das übergebene Objekt wird kontrolliert, ob es ein EinzelteilLegoset ist und ob der EinzelteilLegoset schon in 
     der Datenbank vorhanden ist, falls alles passt, dann wird der neue EinzelteilLegoset hinzugefügt. Es wird je nach
     Fall eine dementsprechende Meldung geprintet"""

    def fuge_einzelteil_legoset_hinzu(self, einzelteil_legoset):
        with self.Session() as session:
            with session.begin():
                for i in einzelteil_legoset:
                    result = "Das übergebene Objekt ist kein EinzelteilLegoset"
                    if isinstance(i, entities.EinzelteilLegoset):
                        """Hier wird kontrolliert, ob der zusammengesetzter Schlüssel vom EinzelteilLegoset schon in der
                                            Datenbank vorhanden ist"""
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

    """Das übergebene Objekt wird kontrolliert, ob es ein Anbieter ist und ob der Anbieter schon in der Datenbank 
     vorhanden ist, falls alles passt, dann wird der neue Anbieter hinzugefügt. Es wird je nach Fall eine 
     dementsprechende Meldung geprintet"""

    def fuge_anbieter_hinzu(self, anbieter):
        with self.Session() as session:
            with session.begin():
                result = "Das übergebene Objekt ist kein Anbieter"
                if isinstance(anbieter, entities.Anbieter):
                    if not session.query(anbieter.__class__).filter(entities.Anbieter.url == anbieter.url).all():
                        session.merge(anbieter)
                        result = "Neuer Anbieter wurde hinzugefügt"
                    else:
                        result = "Anbieter ist schon vorhanden"
                print(result)
                session.commit()
            session.close()

    """Die Liste an Sets, die in der Methode übergeben wurde, wird gelöscht."""

    def loesche_sets(self, sets):
        with self.Session() as session:
            with session.begin():
                for i in sets:
                    session.delete(i)
                session.commit()
            session.close()

    """Hier wird eine Liste übergeben, wo Einzelteile ohne Marktpreise übergeben werden. Hier kann man auch ein Limit
    setzen, wodurch man die Anzahl an Einzelteile begrenzen kann."""

    def einzelteil_ohne_marktpreis(self, limit):
        session = self.Session()
        result = session.query(entities.Einzelteil).outerjoin(entities.Einzelteil.anbieter).filter(entities.EinzelteilMarktpreis.preis.is_(None)).limit(limit)
        return result

    """Zu der übergebenen LegosetID wird eine Liste von all ihren Einzelteilen übergeben"""
    def einzelteile_zu_legoset(self, set_id):
        session = self.Session()
        result = session.query(entities.Einzelteil).join(entities.Einzelteil.sets).filter(entities.EinzelteilLegoset.set_id == set_id)
        return result

    def marktpreise_zu_einzelteile(self, einzelteilliste):
        session = self.Session()
        result = session.query(entities.EinzelteilMarktpreis).join(entities.EinzelteilMarktpreis.einzelteile).filter(entities.EinzelteilMarktpreis.einzelteil_id == i.einzelteil_id)
        return result

    def legosets_zu_name(self, name):
        session = self.Session()
        result = session.query(entities.Legoset).filter(entities.Legoset.name.like("%{}%".format(name))).all()
        return result


