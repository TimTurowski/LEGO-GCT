import multiprocessing
import os
import datetime
from multiprocessing import Process

from pdfminer.high_level import extract_text
from source.anleitungs_downloader.pdf_downloader import PdfDownloader
from source.crawler.set_crawler import SetCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
from source.parser.pdfparser import PDFParser
from source.utility.set_update_logger import SetUpdateLogger


def search_sets(set_crawler, conn2):
    result = set_crawler.crawl_unreleased_sets()
    conn2.send(result)

def execute_download(set_id, conn2):
    p = PdfDownloader()
    download_result = p.download_anleitung(set_ids=[set_id], save_path="./temp_downloader/")
    conn2.send(download_result)
    p.cut_anleitungen(source_path="./temp_downloader/", destination_path="./temp_downloader/", cut_pages=15)

def remove_pdfs(path):
    try:
        if not os.path.isdir(path):
            raise ValueError("Der angegebene Pfad ist kein Verzeichnis.")
        for file in os.listdir(path):
            os.remove(path + file)
        print(f"Der Ordner '{path}' wurde erfolgreich geleert.")
    except Exception as e:
        print(f"Fehler beim Leeren des Ordners: {str(e)}")


if __name__ == "__main__":
    """erster Step aktualisieren der Watchlist"""
    starttime = datetime.datetime.now()
    conn1, conn2 = multiprocessing.Pipe()
    p = Process(target=search_sets, args=(SetCrawler(), conn2))
    p.start()
    p.join()
    set_crawl_result = conn1.recv()
    update_logger = SetUpdateLogger("watchlist.csv")
    update_logger.update_sets(crawl_result=set_crawl_result)
    sets = update_logger.get_sets()

    setcount = 0
    """2. Step versuchen vom Herunterladen von Sets der Watchlist"""
    for set in sets:
        remove_pdfs("./temp_downloader/")

        conn1, conn2 = multiprocessing.Pipe()
        p = Process(target=execute_download, args=(set[0],conn2))
        p.start()
        p.join()
        download_result = conn1.recv()



        pdfparser = PDFParser()
        stueckliste = None

        files = os.listdir("./temp_downloader/")
        dao = Datenzugriffsobjekt()
        for file in files:

            if file.endswith("-cut.pdf"):
                URL = extract_text(r"../geschaeftslogik/temp_downloader/" + str(file))
                stueckliste = PDFParser.parse_text(pdfparser, URL, set[0], set[1])
                print(file)
                if len(stueckliste.stueckliste) > 0:
                    break
        if stueckliste is not None and len(stueckliste.stueckliste) == 0:

            for file in files:

                if not file.endswith("-cut.pdf"):
                    URL = extract_text(r"../geschaeftslogik/temp_downloader/" + str(file))
                    stueckliste = PDFParser.parse_text(pdfparser, URL, set[0], set[1])
                    print(file)
                    if len(stueckliste.stueckliste) > 0:
                        break

        print((datetime.datetime.now() - starttime).total_seconds())

        if stueckliste is not None and len(stueckliste.stueckliste) > 0:
            dao.fuge_einzelteil_legoset_hinzu(stueckliste.stueckliste)
            print(stueckliste)
            print(f"{download_result.succesful_sets[0]} wurde erfolgreich in die Datenbank hinzugefügt")
            update_logger.remove_succesful_sets(download_result.succesful_sets[0])

        setcount = setcount + 1
        print(f"{setcount}/{len(sets)} " + "{:4.2f}".format(setcount*100/len(sets))+"%")