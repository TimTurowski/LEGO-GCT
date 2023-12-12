import os

if(os.name == 'posix'):
    from Entity.entities import EinzelteilLegoset, Einzelteil, Legoset
else:
    from source.Entity.entities import EinzelteilLegoset, Einzelteil, Legoset


class Stueckliste:
    """
    Objekte dieser Klasse speichern Informationen zu Stücklisten
    """
    def __init__(self):
        self.set_id = ""
        self.name = ""
        self.stueckliste = []
    
    def add_to_stueckliste(self, anzahl, einzelteil_id, set_id, name):
        """
        Diese Funktion fügt ein weiteres LegoEinzelteil der Stückliste hinzu, hierzu werden übergebene Informationen
        erst zu einem EinzelteilLegoset Objekt zusammengefügt
        :param anzahl: Wie oft das LegoEinzelteil in dem Set vorkommt
        :type anzahl: int
        :param einzelteil_id: Die Einzelteil_ID
        :type einzelteil_id: string
        :param set_id: Die Set_ID, dem diese Einzelliste zugehörig ist
        :type set_id: string
        :param name: Name des LegoSets
        :type name: string
        """
        eintrag = EinzelteilLegoset(set=Legoset(set_id=set_id, name=name),
                                    einzelteile=Einzelteil(einzelteil_id=einzelteil_id),
                                    anzahl=anzahl)
        self.stueckliste.append(eintrag)
        self.set_id = set_id
        self.name = name

    def print_stueckliste(self):
        """
        Diese Funktion dient der Bildschrirmausgabe der Stückliste
        """
        for eintrag in self.stueckliste:
            print(eintrag)

    def __str__(self):
        result = ""
        for i in self.stueckliste:
            result = result + str(i) + "\n"

        return result



