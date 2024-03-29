import re
import os
from pdfminer.high_level import extract_pages, extract_text
import PyPDF2

if(os.name == 'posix'):
    from parser.stueckliste import Stueckliste
    from utility.converter import clean_line
else:
    from source.parser.stueckliste import Stueckliste
    from source.utility.converter import clean_line



class PDFParser:
    """
    Objekte dieser Klasse besitzen Methoden zum Parsen von PDF-Dateien
    """
    def __init__(self):
        pass
    

    def cut_pdf(URL):
        """
        Diese Funktion schneidet die letzten 10 Seiten der PDF-Datei ab und gibt diese als seperate PDF-Datei zurück
        """
        with open(URL, 'rb') as file:
            pdfReader = PyPDF2.PdfFileReader(file)
            totalPages = pdfReader.getNumPages()
            pdfWriter = PyPDF2.PdfFileWriter()

            if totalPages <= 10:
                raise Exception("Die PDF-Datei ist zu klein, um sie zu der Stückliste zu kürzen.")

            for pages in range(totalPages -10, totalPages):
                page = pdfReader.getPage(pages)
                pdfWriter.addPage(page)
            stueckliste_pdf = pdfWriter
            return stueckliste_pdf 
        

    def parse_text(self, URL, set_id, name):
        """
        Diese Funktion parst die PDF URL nach den Einzelteil-Ids und der Häufigkeit und speichert die Informationen
        in die Stückliste
        """
        stueckliste = Stueckliste()
        ##stueckliste_pdf = PDFParser.cut_pdf(URL)
        lines = URL.split('\n')
        num_lines = len(lines)

        i = 0
        while i < num_lines:
            line = lines[i].strip()
            if line.endswith('x') and i + 1 < num_lines:
                next_line = lines[i + 1].strip()
                if (len(next_line) == 7 or len(next_line) == 6) and next_line.isdigit():

                    anzahl = (line[:-1])
                    anzahl = clean_line(anzahl)
                    einzelteil_id = next_line
                    stueckliste.add_to_stueckliste(anzahl, str(einzelteil_id), set_id, name)
                    i += 1  # Skip the next line since it has been processed
            i += 1
        return stueckliste
  