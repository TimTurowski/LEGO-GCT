import datetime

from pdfparser import PDFParser
from stueckliste import Stueckliste
from pdfminer.high_level import extract_pages, extract_text

# Main-Klasse, um den Parser auszutesten
def main():
    start_time = datetime.datetime.now()
    pdfparser = PDFParser()
    stueckliste = Stueckliste()
    URL = extract_text(r"../anleitungen/6442573-cut.pdf")
    stueckliste = PDFParser.parse_text(pdfparser, URL)
    print((datetime.datetime.now() - start_time).total_seconds())
    print(stueckliste)

if __name__ == "__main__":
    main()