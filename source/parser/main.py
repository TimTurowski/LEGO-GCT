import datetime
import sys
sys.path.append('C:\\Users\\denni\Documents\\GitHub\\LEGO-GCT')
import source
from pdfparser import PDFParser
from stueckliste import Stueckliste
from pdfminer.high_level import extract_text

# Main-Klasse, um den Parser auszutesten
def main():
    start_time = datetime.datetime.now()
    pdfparser = PDFParser()
    stueckliste = Stueckliste()
    URL = extract_text(r"/Users/denni/Desktop/lego_url")
    stueckliste = PDFParser.parse_text(pdfparser, URL, 717171, "Beispielname")
    print((datetime.datetime.now() - start_time).total_seconds())
    print(stueckliste)

if __name__ == "__main__":
    main()