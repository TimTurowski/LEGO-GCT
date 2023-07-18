from sqlalchemy import String, ForeignKey, Column,FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
from sqlalchemy.types import Date

Base = declarative_base()

einzelteil_legoset = Table("einzelteil_legoset",
                          Base.metadata,
                          Column("set_id", ForeignKey("Legoset.set_id")),
                          Column("einzelteil_id", ForeignKey("Einzelteil.einzelteil_id")))

class Legoset (Base):
    __tablename__ = "Legoset"

    set_id = Column(String, primary_key=True)
    name = Column(String)
    zeitpunkt = Column(Date)
    einzelteile = relationship("Einzelteil", secondary=einzelteil_legoset, backref="legosets")

    def __repr__(self):
        f"{self.set_id} {self.name}"

class Einzelteil (Base):
    __tablename__ = "Einzelteil"

    einzelteil_id = Column(String, primary_key=True)
    zeitpunkt = Column(Date)

    def __repr__(self):
        f"{self.einzelteil_id}"

class EinzelteilMarktpreis (Base):
    __tablename__ = "EinzelteilMarktpreis"

    einzelteil_id = Column(ForeignKey("Einzelteil.einzelteil_id"), primary_key=True)
    anbieter_url = Column(ForeignKey("Anbieter.url"), primary_key=True)
    preis = Column(FLOAT)
    url = Column(String)
    einzelteile = relationship("Einzelteil", backref="anbieter_marktpreise")
    anbieter = relationship("Anbieter", backref="einzelteile_preise")

    def __repr__(self):
        f"({self.einzelteil_id} {self.anbieter_url}) {self.preis} {self.url}"

class SetMarktpreis (Base):
    __tablename__ = "SetMarktpreis"

    set_id = Column(ForeignKey("Legoset.set_id"), primary_key=True)
    anbieter_url = Column(ForeignKey("Anbieter.url"), primary_key=True)
    preis = Column(FLOAT)
    url = Column(String)
    sets = relationship("Legoset", backref="anbieter_marktpreise")
    anbieter = relationship("Anbieter", backref="set_preise")

    def __repr__(self):
        f"({self.set_id} {self.anbieter_url}) {self.preis} {self.url}"

class Anbieter (Base):
    __tablename__ = "Anbieter"

    url = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        f"{self.url} {self.name}"
