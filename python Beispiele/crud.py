from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base
from model import Einzelteil

"""Beispiel für einen Datenbank zugriff"""

"""dialect+driver://username:password@host:port/database
"""

"""baut verbidung zur Datenbank auf wenn man in der VPN ist"""

engine = create_engine("postgresql+psycopg2://postgres:27R569RX@192.168.198.47:5432/legoSampel")

"""erstellt Tabelle für das Objekt Einzelteil"""
# Base.metadata.create_all(engine)

"""fügt einzelteil zur Datenbank hinzu"""
def add_einzelteil(einzelteil):
    Session = sessionmaker(bind=engine)
    s = Session()
    s.add(einzelteil)
    s.commit()
    s.close()


"""gibt alle Einzelteile der DB zurück als List"""
def query_einzelteile():
    Session = sessionmaker(bind=engine)
    s = Session()
    return s.query(Einzelteil).all()


"""gibt Einzelteil zur gegebenen ID zurück"""
def query_einzelteile_mit_id():
    Session = sessionmaker(bind=engine)
    s = Session()
    return s.query(Einzelteil).filter(Einzelteil.element_id=="6429055").first()


# einzelteil = Einzelteil(element_id="6435930", name="ROOF TILE 2X3/25° INV.")
# add_einzelteil(einzelteil)

print(query_einzelteile_mit_id().name)
