from datenzugriffsobjekt import Session
from source.Entity import entities

def einzelteilliste():
    session = Session()
    result = session.query(entities.Einzelteil).all()
    return result

