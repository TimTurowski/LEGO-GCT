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
        result = session.query(entities.EinzelteilMarktpreis).filter(entities.EinzelteilMarktpreis.einzelteile == einzelteil).all()
        if not result:
            result = "Einzelteil ist nicht in der Datenbank oder hat keine gecrawlten Preise"
    else:
        result = "Übergebenes Objekt ist kein Legoset"
    return result

"""def einspeisen(entität):
    session = Session()
    result = "Objekt enspricht keinem Datenbankobjekt"
    if isinstance(entität,entities.SetMarktpreis):
        session.query(entität)
        if
        session.begin()
        session.add(entität)
        session.commit()
        session.close()
        result = "War erfolgreich"
    if isinstance(entität,entities.EinzelteilMarktpreis):

    if isinstance(entität,entities.EinzelteilLegoset):

    if isinstance(entität,entities.Anbieter):
    return result"""