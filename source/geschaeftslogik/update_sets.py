import multiprocessing
import os
import datetime
import sys
from multiprocessing import Process
from pdfminer.high_level import extract_text

if(os.name == 'posix'):
    sys.path.append("..")
    from DiscordBot.dc_message import send_discord_message
    from anleitungs_downloader.pdf_downloader import PdfDownloader
    from crawler.set_crawler import SetCrawler
    from datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
    from parser.pdfparser import PDFParser
    from utility.set_update_logger import SetUpdateLogger

    DOWNLOAD_PATH = "/home/student/LEGO-GCT/source/geschaeftslogik/temp_downloader/"
    WATCHLIST_PATH = "/home/student/LEGO-GCT/source/geschaeftslogik/watchlist.csv"
else:
    from source.DiscordBot.dc_message import send_discord_message
    from source.anleitungs_downloader.pdf_downloader import PdfDownloader
    from source.crawler.set_crawler import SetCrawler
    from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
    from source.parser.pdfparser import PDFParser
    from source.utility.set_update_logger import SetUpdateLogger

    DOWNLOAD_PATH = "./temp_downloader/"
    WATCHLIST_PATH = "watchlist.csv"


def search_sets(set_crawler, conn2):
    """
    Diese Funktion sucht nach neuen Legosets und sendet diese in conn2
    :param set_crawler: Ein SetCrawler Objekt
    :type set_crawler: SetCrawler
    :param conn2: eine Connection für Multiprocessing
    :type conn2: multiprocessing.Pipe
    """
    result = set_crawler.crawl_unreleased_sets()
    conn2.send(result)

def execute_download(set_id, conn2):
    """
    Diese Funktion downloaded die Anleitung-PDFS von einem Legoset
    :param set_id: Die ID des Legosets, dessen Anleitung runtergeladen werden soll
    :type set_id: LegosetID
    :param conn2: eine Connection für Multiprocessing
    :type conn2: multiprocessing.Pipe
    """
    p = PdfDownloader()
    download_result = p.download_anleitung(set_ids=[set_id], save_path=DOWNLOAD_PATH)
    conn2.send(download_result)
    # kürzt die Anleitung PDFs um den Parsingvorgang zu verkürzen
    p.cut_anleitungen(source_path=DOWNLOAD_PATH, destination_path=DOWNLOAD_PATH, cut_pages=15)

def remove_pdfs(path):
    """
    Diese Funktion löscht angegebenes Verzeichnis
    :param path: Pfad zum Verzeichnis, welches gelöscht werden soll
    :type path: string
    """
    try:
        if not os.path.isdir(path):
            raise ValueError("Der angegebene Pfad ist kein Verzeichnis.")
        for file in os.listdir(path):
            os.remove(path + file)
        print(f"Der Ordner '{path}' wurde erfolgreich geleert.")
    except Exception as e:
        print(f"Fehler beim Leeren des Ordners: {str(e)}")


if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    starttime = datetime.datetime.now()
    conn1, conn2 = multiprocessing.Pipe()
    p = Process(target=search_sets, args=(SetCrawler(), conn2))
    p.start()
    p.join()

    set_crawl_result = conn1.recv()
    # als erstes wird die Watchlist aktualisiert
    update_logger = SetUpdateLogger(WATCHLIST_PATH, 10)
    update_logger.update_sets(crawl_result=set_crawl_result)
    sets = update_logger.get_sets()
    print(sets)

    setcount = 0
    for set in sets:
        remove_pdfs(DOWNLOAD_PATH)

        # Versuch, die Anleitungen eines Sets zu downloaden
        conn1, conn2 = multiprocessing.Pipe()
        p = Process(target=execute_download, args=(set[0],conn2))
        p.start()
        p.join()
        download_result = conn1.recv()



        pdfparser = PDFParser()
        stueckliste = None

        files = os.listdir(DOWNLOAD_PATH)
        dao = Datenzugriffsobjekt()
        for file in files:
            # gekürzte PDFs als erstes parsen
            if file.endswith("-cut.pdf"):
                # Text aus Anleitung PDF extrahieren
                URL = extract_text(r"" + DOWNLOAD_PATH + str(file))
                # extrahierten Text auf Stückliste untersuchen/parsen
                stueckliste = PDFParser.parse_text(pdfparser, URL, set[0], set[1])
                print(file)
                if len(stueckliste.stueckliste) > 0:
                    break
        if stueckliste is not None and len(stueckliste.stueckliste) == 0:
            # falls gekürzte PDFs keine Stückliste enthalten die ungekürzten PDFs ansehen
            for file in files:

                if not file.endswith("-cut.pdf"):
                    # Text aus Anleitung PDF extrahieren
                    URL = extract_text(r"" + DOWNLOAD_PATH + str(file))
                    # extrahierten Text auf Stückliste untersuchen/parsen
                    stueckliste = PDFParser.parse_text(pdfparser, URL, set[0], set[1])
                    print(file)
                    if len(stueckliste.stueckliste) > 0:
                        break

        print((datetime.datetime.now() - starttime).total_seconds())

        if stueckliste is not None and len(stueckliste.stueckliste) > 0:
            dao.fuge_einzelteil_legoset_hinzu(stueckliste.stueckliste)

            #send_discord_message(f"```ansi\n[0;32m{set[0]}, {set[1]} wurde erfolgreich der Datenbank hinzugefügt```")
            print(f"{download_result.succesful_sets[0]} wurde erfolgreich in die Datenbank hinzugefügt")
            update_logger.remove_succesful_sets(download_result.succesful_sets[0])

        setcount = setcount + 1
        print(f"{setcount}/{len(sets)} " + "{:4.2f}".format(setcount*100/len(sets))+"%")