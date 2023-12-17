from sqlalchemy import String, ForeignKey, Column, FLOAT, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

"""Von dieser Klasse erben alle Klassen die in die Datenbank überführt werden sollen."""
Base = declarative_base()


class Legoset(Base):
    """Eine Klasse, die ein Legoset repräsentiert und in das Datenbankschema integriert werden kann.

        Diese Klasse wird als ORM-Entität für die Tabelle 'Legoset' in der Datenbank verwendet.
        Sie enthält Informationen über ein Legoset, einschließlich einer eindeutigen ID.

        Attribute:
        - set_id (str): Die eindeutige ID des Einzelteils (Primärschlüssel).
        - sets (relationship): Beziehung zu EinzelteilLegoset für Sets, die dieses Einzelteil enthalten.
        - anbieter (relationship): Beziehung zu EinzelteilMarktpreis für Anbieterpreise dieses Einzelteils.
    """

    # In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen.
    __tablename__ = "Legoset"
    # Diese Attribute werden in der Datenbank als Spalten angezeigt.
    set_id = Column(String, primary_key=True)
    name = Column(String)
    # Diese Attribute dienen zur Deklarierung von der Beziehung und dienen als Ablage von den jeweiligen Objekten zum
    # einfügen in die Datenbank. Diese werde nicht in der Datenbank angezeigt ist jedoch in Pythoncode zugreifbar.
    einzelteile = relationship("EinzelteilLegoset", back_populates="set", cascade="all, delete-orphan")
    anbieter = relationship("SetMarktpreis", back_populates="set", cascade="all, delete-orphan")

    def __str__(self):
        return "Legoset ID: " + self.set_id \
            + " Name: " + self.name

    def __repr__(self):
        return f"{self.set_id} {self.name}"


class Einzelteil(Base):
    """Eine Klasse, die ein Einzelteil repräsentiert und in das Datenbankschema integriert werden kann.

        Diese Klasse wird als ORM-Entität für die Tabelle 'Einzelteil' in der Datenbank verwendet.
        Sie enthält Informationen über ein Einzelteil, einschließlich einer eindeutigen ID.

        Attribute:
        - einzelteil_id (str): Die eindeutige ID des Einzelteils (Primärschlüssel).
        - sets (relationship): Beziehung zu EinzelteilLegoset für Sets, die dieses Einzelteil enthalten.
        - anbieter (relationship): Beziehung zu EinzelteilMarktpreis für Anbieterpreise dieses Einzelteils.
    """
    # In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen.
    __tablename__ = "Einzelteil"
    # Dieses Attribut wird in der Datenbank als Spalte angezeigt.
    einzelteil_id = Column(String, primary_key=True)

    sets = relationship("EinzelteilLegoset", back_populates="einzelteile", cascade="all, delete-orphan")
    anbieter = relationship("EinzelteilMarktpreis", back_populates="einzelteile", cascade="all, delete-orphan")

    def __str__(self):
        return "ElementId: " + self.einzelteil_id

    def __repr__(self):
        return f"{self.einzelteil_id}"


class Anbieter(Base):

    __tablename__ = "Anbieter"

    url = Column(String, primary_key=True)
    name = Column(String)

    sets = relationship("SetMarktpreis", back_populates="anbieter", cascade="all, delete-orphan")
    einzelteile = relationship("EinzelteilMarktpreis", back_populates="anbieter", cascade="all, delete-orphan")

    def __str__(self):
        return "Anbieter URL: " + self.url \
            + " Name: " + self.name

    def __repr__(self):
        return f"{self.url} {self.name}"


class Einzelteildetails(Base):

    __tablename__ = "Einzelteildetails"

    sonderteil_id = Column(String, ForeignKey("Einzelteil.einzelteil_id", ondelete="CASCADE"), primary_key=True)
    beschreibung = Column(String)
    farbe = Column(String)
    kategorie_id = Column(String, ForeignKey("Kategorie.kategorie_id", ondelete="CASCADE"))

    kategorie = relationship("Kategorie")
    einzelteile = relationship("Einzelteil")

    def __eq__(self, other):
        return self.einzelteile.einzelteil_id == other.einzelteile.einzelteil_id

    def __hash__(self):
        return int(self.einzelteile.einzelteil_id)

    def __str__(self):
        return ("Einzelteil: " + self.einzelteile.einzelteil_id
                + "Beschreibung: " + self.beschreibung
                + "Farbe: " + self.farbe
                + "Kategorie: " + self.kategorie.kategorie_id)

    def __repr__(self):
        return f"{self.sonderteil_id}, {self.beschreibung},{self.farbe}, {self.kategorie_id}"


class Kategorie(Base):

    __tablename__ = "Kategorie"

    kategorie_id = Column(String, primary_key=True)

    def __str__(self):
        return "Kategorie: " + self.kategorie_id

    def __repr__(self):
        return f"{self.kategorie_id}"


class SetBild(Base):

    __tablename__ = "SetBild"

    set = Column(String, ForeignKey("Legoset.set_id", ondelete="CASCADE"), primary_key=True)
    set_bild = Column(String)

    def __str__(self):
        return "Legoset ID: " + self.set_id

    def __repr__(self):
        return f"{self.set_id}"


class EinzelteilLegoset(Base):
    """
    Eine Klasse EinzelteilLegoset wird erstellt, die später so ins Datenbankschema überführt wird. Dies dient zur
    Darstellung der ManyToMany Beziehung zwischen Legosets und Einzelteile und hat als weitere Informationen die
    Anzahl der jeweiligen Einzelteile und Legosets.
    """

    # In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen.
    __tablename__ = "Einzelteil_legoset"
    # Diese Attribute werden in der Datenbank als Spalten angezeigt.
    einzelteil_id = Column(String, ForeignKey("Einzelteil.einzelteil_id", ondelete="CASCADE"), primary_key=True)
    set_id = Column(String, ForeignKey("Legoset.set_id", ondelete="CASCADE"), primary_key=True)
    anzahl = Column(Integer)

    # Diese Attribute dienen zur Deklarierung von der Beziehung und dienen als Ablage von den jeweiligen Objekten zum
    # einfügen in die Datenbank. Diese werde nicht in der Datenbank angezeigt ist jedoch in Pythoncode zugreifbar.
    einzelteile = relationship("Einzelteil", back_populates="sets")
    set = relationship("Legoset", back_populates="einzelteile")

    def __str__(self):
        return "Einzelteil: " + self.einzelteile.einzelteil_id \
            + " Legoset: " + self.set.set_id \
            + " Anzahl des Einzelteil im Legoset: " + str(self.anzahl)

    def __repr__(self):
        return f"({self.einzelteile.einzelteil_id} {self.set.set_id}) {self.anzahl}"


class EinzelteilMarktpreis(Base):
    """
    Eine Klasse EinzelteilMarktpreis wird erstellt, die später so ins Datenbankschema überführt wird. Dies dient zur
    Darstellung der ManyToMany Beziehung zwischen Anbieter und Einzelteile und hat als weitere Informationen den
    Preis der jeweiligen Einzelteile vom Anbieter, so wie die URL des Einzelteils beim Anbieter.
    """

    # In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen.
    __tablename__ = "EinzelteilMarktpreis"
    # Diese Attribute werden in der Datenbank als Spalten angezeigt.
    einzelteil_id = Column(String, ForeignKey("Einzelteil.einzelteil_id", ondelete="CASCADE"), primary_key=True)
    anbieter_url = Column(String, ForeignKey("Anbieter.url", ondelete="CASCADE"), primary_key=True)
    preis = Column(FLOAT(precision=10, asdecimal=True, decimal_return_scale=2))
    url = Column(String)
    # Diese Attribute dienen zur Deklarierung von der Beziehung und dienen als Ablage von den jeweiligen Objekten zum
    # einfügen in die Datenbank. Diese werde nicht in der Datenbank angezeigt ist jedoch in Pythoncode zugreifbar.
    einzelteile = relationship("Einzelteil", back_populates="anbieter")
    anbieter = relationship("Anbieter", back_populates="einzelteile")

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

    # In der Datenbank anzuzeigender Name so wie Ansprechmöglichkeit in Befehlen.
    __tablename__ = "SetMarktpreis"
    # Diese Attribute werden in der Datenbank als Spalten angezeigt
    set_id = Column(String, ForeignKey("Legoset.set_id", ondelete="CASCADE"), primary_key=True)
    anbieter_url = Column(String, ForeignKey("Anbieter.url", ondelete="CASCADE"), primary_key=True)
    preis = Column(FLOAT(precision=10, asdecimal=True, decimal_return_scale=2))
    url = Column(String)
    # Diese Attribute dienen zur Deklarierung von der Beziehung und dienen als Ablage von den jeweiligen Objekten zum
    # einfügen in die Datenbank. Diese werde nicht in der Datenbank angezeigt ist jedoch in Pythoncode zugreifbar.
    set = relationship("Legoset", back_populates="anbieter")
    anbieter = relationship("Anbieter", back_populates="sets")

    def __str__(self):
        return "Einzelteil: " + self.set.set_id \
            + " Anbieter: " + self.anbieter.url \
            + " Preis: " + "{:4.2f}".format(self.preis) + " €" \
            + " Url: " + self.url

    def __repr__(self):
        return f"({self.set.set_id} {self.anbieter}) {self.preis} {self.url}"
