from sqlalchemy import create_engine, String, ForeignKey, Column, CHAR, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import Table
from typing import List

"""Definierung der Base zum späteren einfügen alle vererbenden Klassen"""
Base = declarative_base()

"""Many to Many Beziehungen konfigurieren mittels extra Tabellen die keine Klassen sind"""
einzelteil_legoset = Table("einzelteil_legoset",
                          Base.metadata,
                          Column("set_id", ForeignKey("Legoset.set_id")),
                          Column("einzelteil_id", ForeignKey("Einzelteil.einzelteil_id")))
anbieter_legoset = Table("anbieter_legoset",
                         Base.metadata,
                         Column("anbieter_id", ForeignKey("Anbieter.url")),
                         Column("set_id", ForeignKey("Legoset.set_id")))
anbieter_einzelteil = Table("anbieter_einzelteil",
                            Base.metadata,
                            Column("anbieter_id", ForeignKey("Anbieter.url")),
                            Column("einzelteil_id", ForeignKey("Einzelteil.einzelteil_id")))


"""erstellen von Klassen die später in die Datenbank kommen soll"""
class Einzelteil(Base):
    __tablename__ = "Einzelteil"

    einzelteil_id = Column(String, primary_key =True)
    name = Column(String)

    def __repr__(self):
        return f"{self.name} {self.einzelteilID}"

class Legoset(Base):
    __tablename__ = "Legoset"

    set_id = Column(String, primary_key=True)
    verfügbarkeit = Column(BOOLEAN)
    anleitung_url = Column(String)
    einzelteile = relationship("Einzelteil", secondary=einzelteil_legoset, backref="legosets")

    def __repr__(self):
        return f"{self.set_id} {self.verfügbarkeit} {self.anleitung_url}"

class Anbieter(Base):
    __tablename__ = "Anbieter"

    url = Column(String, primary_key=True)
    name = Column(String)
    legosets = relationship("Legoset", secondary=anbieter_legoset, backref="anbieter")
    einzelteile = relationship("Einzelteil", secondary=anbieter_einzelteil, backref="anbieter")

    def __repr__(self):
        return f"{self.url} {self.name}"

"""Erstellen einer Verbindung zur Datenbank"""
engine = create_engine("postgresql+psycopg2://postgres:27R569RX@192.168.198.47:5432/legoSampel")
"""Automatisches einfügen von allen definierten Klassen in die Datenbank"""
"""Base.metadata.create_all(bind=engine)"""
Session = sessionmaker(engine)
"""e1 = Einzelteil(einzelteil_id="612",name="Cooler Baustein")
e2 = Einzelteil(einzelteil_id="213",name="Nicht so Cooler Baustein")
l1 = Legoset(set_id="3", verfügbarkeit=False, anleitung_url="www.hi.de",einzelteile=[e1,e2])
with Session() as session:
    with session.begin():
        session.add(e1)
        session.add(e2)
        session.add(l1)
        session.add(Anbieter(url="www.lego.com",name="Lego"))
        session.commit()
    session.close()

with Session() as session:
    with session.begin():
        l1 = session.query(Legoset).first()
        a1 = session.query(Anbieter).filter(Anbieter.name == "Lego").first()
        a1.legosets.append(l1)
        session.commit()
    session.close()"""

with Session() as session:
    with session.begin():
        e1 = session.query(Einzelteil).filter(Einzelteil.einzelteil_id == "612").first()
        e2 = session.query(Einzelteil).filter(Einzelteil.einzelteil_id == "213").first()
        a1 = session.query(Anbieter).filter(Anbieter.name == "Lego").first()
        a1.einzelteile.append(e2)
        session.commit()
    session.close()