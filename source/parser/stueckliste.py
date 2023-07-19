class Stueckliste:
    def __init__(self):
        self.anzahl
        self.set_einzelteil_id
        self.stueckliste = {()}

    def set_anzahl(self, anzahl):
        self.anzahl = anzahl

    def set_einzelteil_id(self, einzelteil_id):
        self.einzelteil_id = einzelteil_id

    def add_to_stueckliste(self, anzahl, einzelteil_id):
        self.stueckliste = self.stueckliste.add((anzahl, einzelteil_id))


    #def print_stueckliste(self):
        #for tupel in self.stueckliste:
            #print(f"Anzahl: {teile.anzahl}, Einzelteil-ID: {bauteil.einzelteil_id}")