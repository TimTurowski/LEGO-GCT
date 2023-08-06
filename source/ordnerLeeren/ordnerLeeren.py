import os
import shutil

def leere_ordner(ordner_pfad):
    try:
        # Überprüfen, ob der angegebene Pfad ein Verzeichnis ist
        if not os.path.isdir(ordner_pfad):
            raise ValueError("Der angegebene Pfad ist kein Verzeichnis.")
        
        # Lösche alle Dateien im Ordner
        for datei in os.listdir(ordner_pfad):
            datei_pfad = os.path.join(ordner_pfad, datei)
            if os.path.isfile(datei_pfad):
                os.remove(datei_pfad)
            elif os.path.isdir(datei_pfad):
                shutil.rmtree(datei_pfad)  # Lösche das Unterverzeichnis rekursiv

        print(f"Der Ordner '{ordner_pfad}' wurde erfolgreich geleert.")
    except Exception as e:
        print(f"Fehler beim Leeren des Ordners: {str(e)}")

# Beispielaufruf
ordner_pfad = "C:\Users\t.turowski\Documents\LEGO-GCT\source\ordnerLeeren/Testordner"
leere_ordner(ordner_pfad)