import re
import stueckliste
from pdfminer.high_level import extract_pages, extract_text

#for page_layout in extract_pages(r"c:\Users\denni\Desktop\lego_url.pdf"):
#     for element in page_layout:
#         print(element)

URL = extract_text(r"c:\Users\denni\Desktop\lego_url.pdf")
#print(URL)
stueckliste = Stueckliste()
class Parsser:
    def parse_text(URL):
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
        print(stueckliste)
        return stueckliste
    
    #for teile in stueckliste.stueckliste:
        #print(f"Anzahl: {}")

    #legoset = parse_text(URL)
    #for bauteil in legoset.bauteile:
        #print(f"Anzahl: {bauteil.anzahl}, Einzelteil-ID: {bauteil.einzelteil_id}")