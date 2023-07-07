"""Die Klasse EinzelTeilMarktpreis repräsentiert ein Objekt, welches zu einem Einzelteil den jeweiligen Preis verwaltet
zudem wird der Zeitpunkt gespeiichert wann der Preis Gecrawlt wurde. Desweiteren wird auch die Url gespeichert wo der
Preis gecrawlt wurde(für spätere Updates)"""
class EinzelTeilMarktpreis:
    """Bestand ist standard mässig auf None, da die Meisten Shops keine Bestands angabe machen"""

    """
    TODO 
    - Objektrelationales Modell erstellen
    - umgang mit Bestand diskutieren
    """
    def __init__(self, einzelteil, preis, zeitpunkt, url, bestand = None):
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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__preis == other.__preis and \
                self.__einzelteil == other.__einzelteil and \
                self.__url == other.__url
        else:
            return False