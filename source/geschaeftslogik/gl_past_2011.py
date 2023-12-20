import datetime
import os
from multiprocessing import Process
from pdfminer.high_level import extract_text

if(os.name == 'posix'):
    from anleitungs_downloader.pdf_downloader import PdfDownloader
    from datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
    from parser.pdfparser import PDFParser
    from utility.set_logger import SetLogger
else:
    from source.anleitungs_downloader.pdf_downloader import PdfDownloader
    from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
    from source.parser.pdfparser import PDFParser
    from source.utility.set_logger import SetLogger

TEMP_DOWNLOADER_PATH = "/home/student/LEGO-GCT/source/geschaeftslogik/temp_downloader/"
def execute_download(set_id):
    p = PdfDownloader()
    print(p.download_anleitung(set_ids=[set_id], save_path=TEMP_DOWNLOADER_PATH))
    p.cut_anleitungen(source_path=TEMP_DOWNLOADER_PATH, destination_path=TEMP_DOWNLOADER_PATH, cut_pages=15)

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
    """PDF Download"""
    if not os.path.exists(TEMP_DOWNLOADER_PATH):
        os.makedirs(TEMP_DOWNLOADER_PATH)
    sl = SetLogger()
    starttime = datetime.datetime.now()
    years = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
    for year in years:
        remaining_sets = sl.missing_set_log(year=year)
        setcount = 0
        for set in remaining_sets:
            remove_pdfs(TEMP_DOWNLOADER_PATH)

            # nächstes verfügbare Set

            p = Process(target=execute_download, args=(set[0],))
            p.start()
            p.join()

            pdfparser = PDFParser()
            stueckliste = None

            files = os.listdir(TEMP_DOWNLOADER_PATH)
            dao = Datenzugriffsobjekt()
            for file in files:

                if file.endswith("-cut.pdf"):
                    URL = extract_text(TEMP_DOWNLOADER_PATH + str(file))
                    stueckliste = PDFParser.parse_text(pdfparser, URL, set[0], set[1])
                    print(file)
                    # print(stueckliste)
                    if len(stueckliste.stueckliste) > 0:
                        sl.add_succesful_set(set[0], set[1], year)
                        break
            if stueckliste is not None and len(stueckliste.stueckliste) == 0:

                for file in files:

                    if not file.endswith("-cut.pdf"):
                        URL = extract_text(TEMP_DOWNLOADER_PATH + str(file))
                        stueckliste = PDFParser.parse_text(pdfparser, URL, set[0], set[1])
                        print(file)
                        if len(stueckliste.stueckliste) > 0:
                            sl.add_succesful_set(set[0], set[1], year)
                            break


            print((datetime.datetime.now() - starttime).total_seconds())

            if stueckliste is not None and len(stueckliste.stueckliste) > 0:
                dao.fuge_einzelteil_legoset_hinzu(stueckliste.stueckliste)
            else:
                sl.add_failed_set(set[0], set[1], year)
            setcount = setcount + 1
            dao.Session.close_all()
            print(f"{setcount}/{len(remaining_sets)}  {setcount * 100/len(remaining_sets)}%")







