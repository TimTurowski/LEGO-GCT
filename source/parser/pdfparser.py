import re
import source
from stueckliste import Stueckliste
from pdfminer.high_level import extract_pages, extract_text
import PyPDF2

stueckliste = Stueckliste()
# Klasse des PDFParsers
class PDFParser:
    def __init__(self):
        pass
    
    # Schneidet die letzten 10 Seiten der PDF-Datei ab und gibt diese als seperate PDF-Datei zurück
    def cut_pdf(URL):
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
        
    # Parst die PDF "URL" nach den Einzelteil-Ids und der Häufigkeit und speichert die Informationen in die Stücklist
    def parse_text(self, URL, set_id, name):
        stueckliste_pdf = PDFParser.cut_pdf(URL)
        lines = stueckliste_pdf.split('\n')
        num_lines = len(lines)

        i = 0
        while i < num_lines:
            line = lines[i].strip()
            if line.endswith('x') and i + 1 < num_lines:
                next_line = lines[i + 1].strip()
                if (len(next_line) == 7 or len(next_line) == 6) and next_line.isdigit():
                    anzahl = (line[:-1])
                    einzelteil_id = next_line
                    stueckliste.add_to_stueckliste(anzahl, einzelteil_id, set_id, name)
                    i += 1  # Skip the next line since it has been processed
            i += 1
        return stueckliste
  