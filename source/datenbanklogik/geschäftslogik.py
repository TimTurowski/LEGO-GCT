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
            result = "Legoset ist nicht in der Datenbank"
    else:
        result = "Übergebenes Objekt ist kein Legoset"
    return result
