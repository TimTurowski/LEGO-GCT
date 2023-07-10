"""Die Klasse EinzelTeilMarktpreis repräsentiert ein Objekt, welches zu einem Einzelteil den jeweiligen Preis verwaltet,
zudem, wird der Zeitpunkt gespeichert, wann der Preis gecrawlt wurde. Des Weiteren wird auch die Url gespeichert, wo der
Preis gecrawlt wurde(für spätere Updates)"""


class EinzelTeilMarktpreis:
    """Bestand ist standard mässig auf None, da die meisten Shops keine Angaben über den Bestand machen"""

    """
    TODO 
    - Objektrelationales Modell erstellen
    - umgang mit Bestand diskutieren
    """

    def __init__(self, einzelteil, preis, zeitpunkt, url, bestand=None):
        self.__einzelteil = einzelteil
        self.__preis = preis
        self.__zeitpunkt = zeitpunkt
        self.__url = url
        self.__bestand = bestand

    @property
    def einzelteil(self):
        return self.__einzelteil

    @einzelteil.setter
    def einzelteil(self, new_einzelteil):
        self.__einzelteil = new_einzelteil

    @property
    def preis(self):
        return self.__preis

    @preis.setter
    def preis(self, new_preis):
        self.__preis = new_preis

    """Zeitpunkt gibt an wann der Preis gecrawlt wurde"""

    @property
    def zeitpunkt(self):
        return self.__zeitpunkt

    @zeitpunkt.setter
    def zeitpunkt(self, new_zeitpunkt):
        self.__zeitpunkt = new_zeitpunkt

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, new_url):
        self.__url = new_url

    @property
    def bestand(self):
        return self.__bestand

    @bestand.setter
    def bestand(self, new_bestand):
        self.__bestand = new_bestand

    """Equals ignoriert momentan den Zeitpunkt ist in diesen Fall sinnvoll"""

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__preis == other.__preis and \
                self.__einzelteil == other.__einzelteil and \
                self.__url == other.__url
        else:
            return False

    """gibt Textuelle Darstellung von einzelteil Marktpreis"""

    def __str__(self):
        return str(self.__einzelteil) + " Preis: " + str(self.__preis) + "€" + " Zeitpunkt: " + str(
            self.__zeitpunkt) + " Url: " + self.__url
