# Klasse, um die Einträge der Stückliste zu definieren und darzustellen.
class Eintrag:
    def __init__(self, anzahl, einzelteil_id):
        self.anzahl = anzahl
        self.einzelteil_id = einzelteil_id
    
    def print_eintrag(self):
        print(f"Anzahl: {self.anzahl}, Einelteil-ID: {self.einzelteil_id}")