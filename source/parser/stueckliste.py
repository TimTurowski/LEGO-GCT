from eintrag import Eintrag
# Klasse um die Stückliste darzustellen. Inhalt sind die Einträge, welche in Tupel der Form( Tupel(Anzahl, Eintelteil-ID) ) gesetzt werden.
class Stueckliste:
    def __init__(self):
        self.stueckliste = []
    
    def add_to_stueckliste(self, anzahl, einzelteil_id):
        eintrag = Eintrag(anzahl, einzelteil_id)
        self.stueckliste.append(eintrag)

    def print_stueckliste(self):
        for eintrag in self.stueckliste:
            eintrag.print_eintrag()


