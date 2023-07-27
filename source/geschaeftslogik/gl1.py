import os
from multiprocessing import Process
from pdfminer.high_level import extract_text
from source.anleitungs_downloader.pdf_downloader import PdfDownloader
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
from source.parser.pdfparser import PDFParser
from source.parser.stueckliste import Stueckliste


def execute_download():
    p = PdfDownloader()
    print(p.download_anleitung(set_ids=["76155"], save_path="./temp_downloader/"))

if __name__ == "__main__":
    """PDF Download"""
    p = Process(target=execute_download)
    p.start()
    p.join()

    pdfparser = PDFParser()
    stueckliste = Stueckliste()

    files = os.listdir("./temp_downloader/")
    dao = Datenzugriffsobjekt()
    for file in files:
        URL = extract_text(r"./temp_downloader/" + str(file))
        stueckliste = PDFParser.parse_text(pdfparser, URL)

        print(file)
        print(stueckliste)

    dao.fuge_einzelteil_legoset_hinzu(stueckliste.stueckliste)





