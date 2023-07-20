from sqlalchemy import String, ForeignKey, Column, FLOAT, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class EinzelteilLegoset (Base):
    __tablename__ = "Einzelteil_legoset"

    einzelteil_id = Column(ForeignKey("Einzelteil.einzelteil_id"), primary_key=True)
    set_id = Column(ForeignKey("Legoset.set_id"), primary_key=True)
    anzahl = Column(Integer)
    einzelteile = relationship("Einzelteil", backref="einzelteile")
    set = relationship("Legoset", backref="set")

    def __repr__(self):
        return f"({self.einzelteil_id} {self.set_id}) {self.anzahl}"

class Legoset (Base):
    __tablename__ = "Legoset"

    set_id = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"{self.set_id} {self.name}"

class Einzelteil (Base):
    __tablename__ = "Einzelteil"

    einzelteil_id = Column(String, primary_key=True)

    def __str__(self):
        return "ElementId: " + self.einzelteil_id

    def __repr__(self):
        return f"{self.einzelteil_id}"

class EinzelteilMarktpreis (Base):
    __tablename__ = "EinzelteilMarktpreis"

    einzelteil_id = Column(ForeignKey("Einzelteil.einzelteil_id"), primary_key=True)
    anbieter_url = Column(ForeignKey("Anbieter.url"), primary_key=True)
    preis = Column(FLOAT)
    url = Column(String)
    einzelteile = relationship("Einzelteil", backref="anbieter_marktpreise")
    anbieter = relationship("Anbieter", backref="einzelteile_preise")

    def __str__(self):
        return "Einzelteil: " + str(self.einzelteil_id) \
            + " Anbieter: " + str(self.anbieter_url) \
            + " Preis: " + str(self.preis) + "€" \
            + " Url: " + self.url

    def __repr__(self):
        return f"({self.einzelteil_id} {self.anbieter_url}) {self.preis} {self.url}"

class SetMarktpreis (Base):
    __tablename__ = "SetMarktpreis"

    set_id = Column(ForeignKey("Legoset.set_id"), primary_key=True)
    anbieter_url = Column(ForeignKey("Anbieter.url"), primary_key=True)
    preis = Column(FLOAT)
    url = Column(String)
    set = relationship("Legoset", backref="anbieter_marktpreise")
    anbieter = relationship("Anbieter", backref="set_preise")

    def __str__(self):
        return "Einzelteil: " + str(self.set_id) \
            + " Anbieter: " + str(self.anbieter_url) \
            + " Preis: " + str(self.preis) + "€" \
            + " Url: " + self.url

    def __repr__(self):
        return f"({self.set_id} {self.anbieter_url}) {self.preis} {self.url}"

class Anbieter (Base):
    __tablename__ = "Anbieter"

    url = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"{self.url} {self.name}"