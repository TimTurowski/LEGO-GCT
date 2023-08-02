from source.Entity.entities import EinzelteilLegoset, Einzelteil, Legoset

# Klasse um die Stückliste darzustellen. Inhalt sind die Einträge, welche in Tupel der Form( Tupel(Anzahl, Eintelteil-ID) ) gesetzt werden.
class Stueckliste:
    def __init__(self):
        self.set_id = 0
        self.name = ""
        self.stueckliste = []
    
    def add_to_stueckliste(self, anzahl, einzelteil_id, set_id, name):
        # eintrag = Eintrag(anzahl, einzelteil_id)
        """Anpassen auf Entitäten für die Datenbank"""
        eintrag = EinzelteilLegoset(set=Legoset(set_id=set_id, name=name),
                                    einzelteile=Einzelteil(einzelteil_id=einzelteil_id),
                                    anzahl=anzahl)
        self.stueckliste.append(eintrag)
        self.set_id = set_id
        self.name = name

    def print_stueckliste(self):
        for eintrag in self.stueckliste:
            # eintrag.print_eintrag()
            print(eintrag)

    def __str__(self):
        result = ""
        for i in self.stueckliste:
            result = result + str(i) + "\n"

        return result



