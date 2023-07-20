from pdfparser import PDFParser
from stueckliste import Stueckliste
from pdfminer.high_level import extract_pages, extract_text

# Main-Klasse, um den Parser auszutesten
def main():
    pdfparser = PDFParser()
    stueckliste = Stueckliste()
    URL = extract_text(r"c:\Users\denni\Desktop\lego_url.pdf")
    stueckliste = PDFParser.parse_text(pdfparser, URL)
    stueckliste.print_stueckliste()

if __name__ == "__main__":
    main()