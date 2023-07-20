from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from source.Entity import entities
from sqlalchemy import inspect

engine = create_engine("postgresql+psycopg2://postgres:27R569RX@192.168.198.47:5432/LegoGCT")
Session = sessionmaker(engine)

def einzelteilliste():
    session = Session()
    result = session.query(entities.Einzelteil).all()
    return result

def legosetliste():
    session = Session()
    result = session.query(entities.Legoset).all()
    return result

def anbieterliste():
    session = Session()
    result = session.query(entities.Anbieter).all()
    return result

def legosetpreise(legoset):
    session = Session()
    if isinstance(legoset,entities.Legoset):
        result = session.query(entities.SetMarktpreis).filter(entities.SetMarktpreis.set == legoset).all()
        if not result:
            result = "Legoset ist nicht in der Datenbank oder hat keine gecrawlten Preise"
    else:
        result = "Übergebenes Objekt ist kein Legoset"
    return result

def einzelteilpreise(einzelteil):
    session = Session()
    if isinstance(einzelteil, entities.Einzelteil):
        result = session.query(entities.EinzelteilMarktpreis)\
            .filter(entities.EinzelteilMarktpreis.einzelteile == einzelteil).all()
        if not result:
            result = "Einzelteil ist nicht in der Datenbank oder hat keine gecrawlten Preise"
    else:
        result = "Übergebenes Objekt ist kein Legoset"
    return result

def einspeisen(entität):
    session = Session()
    result = "Objekt enspricht keinem Datenbankobjekt"
    session.begin()
    if isinstance(entität,entities.SetMarktpreis):
        session.add(entities.SetMarktpreis(set_id=entität.set.set_id,anbieter_url=entität.anbieter.url,
                                           preis=entität.preis,url=entität.url))
        result = "Neuer SetMarktpreis wurde erfolgreich hinzugefügt"
    if isinstance(entität,entities.EinzelteilMarktpreis):
        einzelteil = session.query(entität.einzelteile.__class__).filter(
            entities.Einzelteil.einzelteil_id == entität.einzelteile.einzelteil_id).all()
        anbieter = session.query(entität.anbieter.__class__).filter(entities.Anbieter.url == entität.anbieter.url).all()
        print(anbieter)
        if not session.query(entität.__class__)\
                .filter(entities.EinzelteilMarktpreis.einzelteil_id == entität.einzelteile.einzelteil_id)\
                .filter(entities.EinzelteilMarktpreis.anbieter_url == entität.anbieter.url).all():
            if einzelteil and anbieter:
                print("tim")
                session.add(
                    entities.EinzelteilMarktpreis(einzelteil_id=entität.einzelteile.einzelteil_id,
                                                  anbieter_url=entität.anbieter.url,url=entität.url,preis=entität.preis)
                )
                result = "Neuer EinzelteilMarktpreis wurde erfolgreich hinzugefügt"
            elif einzelteil or anbieter:
                if einzelteil:
                    print("ok")
                    session.add(
                        entities.EinzelteilMarktpreis(einzelteil_id=entität.einzelteile.einzelteil_id, url=entität.url,
                                                   anbieter=entität.anbieter,preis=entität.preis))
                    result = "Neuer EinzelteilMarktpreis und neuer Anbieter wurde erfolgreich hinzugefügt"
                else:
                    print("hi")
                    session.add(entities.EinzelteilMarktpreis(url=entität.url,einzelteile=entität.einzelteile,
                                                              preis=entität.preis,anbieter=session.query(entität.anbieter.__class__).filter(entities.Anbieter.url == entität.anbieter.url).first()))
                    result = "Neuer EinzelteilMarktpreis und neues Einzelteil wurde erfolgreich hinzugefügt"
            else:
                print("nicht ok")
                session.add(entität)
                result = "Neuer EinzelteilMarktpreis, neues Einzelteil und neues Anbieter wurde erfolgreich hinzugefügt"
        else:
            result = "EinzelteilMarktpreis ist schon vorhanden"
    if isinstance(entität,entities.EinzelteilLegoset):
        einzelteil = session.query(entität.einzelteile.__class__).filter(
            entities.Einzelteil.einzelteil_id == entität.einzelteile.einzelteil_id).all()
        anbieter = session.query(entität.set.__class__).filter(entities.Legoset.set_id == entität.set.set_id).all()
        if einzelteil and anbieter:
            session.add(
                entities.EinzelteilLegoset(einzelteil_id=entität.einzelteile.einzelteil_id,set_id=entität.set.set_id,
                                           anzahl=entität.anzahl))
            result = "Neuer EinzelteilLegoset wurde erfolgreich hinzugefügt"
        elif einzelteil or anbieter:
            if einzelteil:
                session.add(
                    entities.EinzelteilLegoset(einzelteil_id=entität.einzelteile.einzelteil_id,anzahl=entität.anzahl,
                                               set=entität.set))
                result = "Neuer EinzelteilLegoset und neues Legoset wurde erfolgreich hinzugefügt"
            else:
                session.add(entities.EinzelteilLegoset(set_id=entität.set.set_id, anzahl=entität.anzahl,
                                               einzelteile=entität.einzelteile))
                result = "Neuer EinzelteilLegoset und neues Einzelteil wurde erfolgreich hinzugefügt"
        else:
            session.add(entität)
            result = "Neuer EinzelteilLegoset, neues Einzelteil und neues Legoset wurde erfolgreich hinzugefügt"
    if isinstance(entität,entities.Anbieter):
        if not session.query(entität.__class__).filter(entities.Anbieter.url == entität.url).all():
            session.add(entität)
    session.commit()
    session.close()
    return result

def marktpreis_hinzufuegen(marktpreis):

    with Session() as session:

        if not session.query(marktpreis.__class__) \
                .filter(entities.EinzelteilMarktpreis.einzelteil_id == marktpreis.einzelteile.einzelteil_id) \
                .filter(entities.EinzelteilMarktpreis.anbieter_url == marktpreis.anbieter.url).all():
            einzelteil = session.query(entities.Einzelteil).filter(entities.Einzelteil.einzelteil_id == marktpreis.einzelteile.einzelteil_id).first()
            if einzelteil is None:
                einzelteil = marktpreis.einzelteile
            anbieter = session.query(entities.Anbieter).filter(entities.Anbieter.url == marktpreis.anbieter.url).first()
            if anbieter is None:
                anbieter = marktpreis.anbieter
            print(einzelteil)
            print(anbieter)
            print(anbieter in session)
            session.add(entities.EinzelteilMarktpreis(preis=marktpreis.preis,url=marktpreis.url,einzelteile=einzelteil,anbieter=anbieter))
            #session.add(marktpreis)
            session.commit()
            session.close()
