import re
from pdfminer.high_level import extract_pages, extract_text

# for page_layout in extract_pages("/Users/timturowski/Desktop/Bauanleitungen/10323_DE_BI_Build_Translate.pdf"):
#     for element in page_layout:
#         print(element)

text = extract_text("/Users/timturowski/Desktop/Bauanleitungen/6449317.pdf")
#print(text)

class Bauteil:
    def __init__(self, anzahl, einzelteil_id):
        self.anzahl = anzahl
        self.einzelteil_id = einzelteil_id

class Legoset:
    def __init__(self):
        self.bauteile = []

def parse_text(text):
    legoset = Legoset()
    lines = text.split('\n')
    num_lines = len(lines)

    i = 0
    while i < num_lines:
        line = lines[i].strip()
        if line.endswith('x') and i + 1 < num_lines:
            next_line = lines[i + 1].strip()
            if len(next_line) == 7 and next_line.isdigit():
                anzahl = (line[:-1])
                einzelteil_id = next_line
                bauteil = Bauteil(anzahl, einzelteil_id)
                legoset.bauteile.append(bauteil)
                i += 1  # Skip the next line since it has been processed
        i += 1

    return legoset

legoset = parse_text(text)

for bauteil in legoset.bauteile:
    print(f"Anzahl: {bauteil.anzahl}, Einzelteil-ID: {bauteil.einzelteil_id}")