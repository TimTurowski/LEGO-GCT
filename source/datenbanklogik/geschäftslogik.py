from datenzugriffsobjekt import Session
from source.Entity import entities

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
        session.add(
            entities.EinzelteilMarktpreis(einzelteil_id=entität.einzelteile.einzelteil_id,
                                          anbieter_url=entität.anbieter.url,preis=entität.preis,url=entität.url))
        result = "Neuer EinzelteilMarktpreis wurde erfolgreich hinzugefügt"
    if isinstance(entität,entities.EinzelteilLegoset):
        einzelteil = session.query(entität.einzelteile.__class__).filter(
            entities.Einzelteil.einzelteil_id == entität.einzelteile.einzelteil_id).all()
        set = session.query(entität.set.__class__).filter(entities.Legoset.set_id == entität.set.set_id).all()
        if einzelteil and set:
            session.add(
                entities.EinzelteilLegoset(einzelteil_id=entität.einzelteile.einzelteil_id,set_id=entität.set.set_id,
                                           anzahl=entität.anzahl))
            result = "Neuer EinzelteilLegoset wurde erfolgreich hinzugefügt"
        elif einzelteil or set:
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
            session.add(entities.EinzelteilLegoset(entität))
            result = "Neuer EinzelteilLegoset, neues Einzelteil und neues Legoset wurde erfolgreich hinzugefügt"
    if isinstance(entität,entities.Anbieter):
        if not session.query(entität.__class__).filter(entities.Anbieter.url == entität.url).all():
            session.add(entität)
    session.commit()
    session.close()
    return result