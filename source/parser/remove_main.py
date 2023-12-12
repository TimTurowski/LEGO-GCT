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
    URL = extract_text(r"../anleitungen/6131627-cut.pdf")
    stueckliste = PDFParser.parse_text(pdfparser, URL, "111111", "Beispielname")
    print((datetime.datetime.now() - start_time).total_seconds())
    print(stueckliste)

if __name__ == "__main__":
    main()