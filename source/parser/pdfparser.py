import re
from stueckliste import Stueckliste
from pdfminer.high_level import extract_pages, extract_text


stueckliste = Stueckliste()
# Klasse des PDFParsers
class PDFParser:
    def __init__(self):
        pass
    # Parst die PDF "URL" nach den Einzelteil-Ids und der Häufigkeit und speichert die Informationen in die Stückliste    
    def parse_text(self, URL):
        lines = URL.split('\n')
        num_lines = len(lines)

        i = 0
        while i < num_lines:
            line = lines[i].strip()
            if line.endswith('x') and i + 1 < num_lines:
                next_line = lines[i + 1].strip()
                if len(next_line) == 7 and next_line.isdigit():
                    anzahl = (line[:-1])
                    einzelteil_id = next_line
                    stueckliste.add_to_stueckliste(anzahl, einzelteil_id)
                    i += 1  # Skip the next line since it has been processed
            i += 1
        return stueckliste