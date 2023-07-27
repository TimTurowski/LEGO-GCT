from sqlalchemy import String, ForeignKey, Column, FLOAT, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

"""Von dieser Klasse erben alle Klassen die in die Datenbank überführt werden sollen."""
Base = declarative_base()


class Legoset(Base):
    """Eine Klasse Legoset wird erstellt, die später so ins Datenbankschema überführt wird."""

    """In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen."""
    __tablename__ = "Legoset"
    """Diese Attribute werden in der Datenbank als Spalten angezeigt."""
    set_id = Column(String, primary_key=True)
    name = Column(String)

    def __str__(self):
        return "Legoset ID: " + self.set_id \
            + " Name: " + self.name

    def __repr__(self):
        return f"{self.set_id} {self.name}"


class Einzelteil(Base):
    """Eine Klasse Einzelteil wird erstellt, die später so ins Datenbankschema überführt wird."""

    """In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen."""
    __tablename__ = "Einzelteil"
    """Dieses Attribut wird in der Datenbank als Spalte angezeigt."""
    einzelteil_id = Column(String, primary_key=True)

    def __str__(self):
        return "ElementId: " + self.einzelteil_id

    def __repr__(self):
        return f"{self.einzelteil_id}"


class Anbieter(Base):
    """Eine Klasse Anbieter wird erstellt, die später so ins Datenbankschema überführt wird."""

    """In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen."""
    __tablename__ = "Anbieter"
    """Diese Attribute werden in der Datenbank als Spalten angezeigt."""
    url = Column(String, primary_key=True)
    name = Column(String)

    def __str__(self):
        return "Anbieter URL: " + self.url \
            + " Name: " + self.name

    def __repr__(self):
        return f"{self.url} {self.name}"


class EinzelteilLegoset(Base):
    """
    Eine Klasse EinzelteilLegoset wird erstellt, die später so ins Datenbankschema überführt wird. Dies dient zur
    Darstellung der ManyToMany Beziehung zwischen Legosets und Einzelteile und hat als weitere Informationen die
    Anzahl der jeweiligen Einzelteile und Legosets.
    """

    """In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen."""
    __tablename__ = "Einzelteil_legoset"
    """Diese Attribute werden in der Datenbank als Spalten angezeigt."""
    einzelteil_id = Column(String, ForeignKey("Einzelteil.einzelteil_id"), primary_key=True)
    set_id = Column(String, ForeignKey("Legoset.set_id"), primary_key=True)
    anzahl = Column(Integer)
    """
    Diese Attribute dienen zur Deklarierung von der Beziehung und dienen als Ablage von den jeweiligen Objekten zum
    einfügen in die Datenbank. Diese werde nicht in der Datenbank angezeigt ist jedoch in Pythoncode zugreifbar.
    """
    einzelteile = relationship("Einzelteil", backref="einzelteile", lazy="joined")
    set = relationship("Legoset", backref="set", lazy="joined")

    def __str__(self):
        return "Einzelteil: " + self.einzelteile.einzelteil_id \
            + " Legoset: " + self.set.set_id \
            + " Anzahl des Einzelteil im Legoset: " + str(self.anzahl)

    def __repr__(self):
        return f"({self.einzelteil_id} {self.set_id}) {self.anzahl}"


class EinzelteilMarktpreis(Base):
    """
    Eine Klasse EinzelteilMarktpreis wird erstellt, die später so ins Datenbankschema überführt wird. Dies dient zur
    Darstellung der ManyToMany Beziehung zwischen Anbieter und Einzelteile und hat als weitere Informationen den
    Preis der jeweiligen Einzelteile vom Anbieter, so wie die URL des Einzelteils beim Anbieter.
    """

    """In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen."""
    __tablename__ = "EinzelteilMarktpreis"
    """Diese Attribute werden in der Datenbank als Spalten angezeigt."""
    einzelteil_id = Column(String, ForeignKey("Einzelteil.einzelteil_id"), primary_key=True)
    anbieter_url = Column(String, ForeignKey("Anbieter.url"), primary_key=True)
    preis = Column(FLOAT(precision=10, asdecimal=True, decimal_return_scale=2))
    url = Column(String)
    """
    Diese Attribute dienen zur Deklarierung von der Beziehung und dienen als Ablage von den jeweiligen Objekten zum
    einfügen in die Datenbank. Diese werde nicht in der Datenbank angezeigt ist jedoch in Pythoncode zugreifbar.
    """
    einzelteile = relationship("Einzelteil", backref="anbieter_marktpreise", lazy="joined")
    anbieter = relationship("Anbieter", backref="einzelteile_preise", lazy="joined")

    def __str__(self):
        return "Einzelteil: " + self.einzelteile.einzelteil_id \
            + " Anbieter: " + self.anbieter.url \
            + " Preis: " + "{:4.2f}".format(self.preis) + " €" \
            + " Url: " + self.url

    def __repr__(self):
        return f"({self.einzelteile.einzelteil_id} {self.anbieter.url}) {self.preis} {self.url}"


class SetMarktpreis(Base):
    """
    Eine Klasse SetMarktpreis wird erstellt, die später so ins Datenbankschema überführt wird. Dies dient zur
    Darstellung der ManyToMany Beziehung zwischen Anbieter und Legosets und hat als weitere Informationen den Preis der
    jeweiligen Legosets vom Anbieter, so wie die URL des Legosets beim Anbieter.
    """

    """In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen."""
    __tablename__ = "SetMarktpreis"
    """Diese Attribute werden in der Datenbank als Spalten angezeigt"""
    set_id = Column(String, ForeignKey("Legoset.set_id"), primary_key=True)
    anbieter_url = Column(String, ForeignKey("Anbieter.url"), primary_key=True)
    preis = Column(FLOAT(precision=10, asdecimal=True, decimal_return_scale=2))
    url = Column(String)
    """
    Diese Attribute dienen zur Deklarierung von der Beziehung und dienen als Ablage von den jeweiligen Objekten zum
    einfügen in die Datenbank. Diese werde nicht in der Datenbank angezeigt ist jedoch in Pythoncode zugreifbar.
    """
    set = relationship("Legoset", backref="anbieter_marktpreise", lazy="joined")
    anbieter = relationship("Anbieter", backref="set_preise", lazy="joined")

    def __str__(self):
        return "Einzelteil: " + self.set.set_id \
            + " Anbieter: " + self.anbieter.url \
            + " Preis: " + "{:4.2f}".format(self.preis) + " €" \
            + " Url: " + self.url

    def __repr__(self):
        return f"({self.set_id} {self.anbieter_url}) {self.preis} {self.url}"
