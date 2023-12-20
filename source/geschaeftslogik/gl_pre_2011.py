import multiprocessing
import datetime
from multiprocessing import Process
import os

if(os.name == 'posix'):
    from crawler.part_crawler import PartCrawler
    from datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
    from utility.set_logger import SetLogger
else:
    from source.crawler.part_crawler import PartCrawler
    from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
    from source.utility.set_logger import SetLogger

# Definition der Funktion für den Crawl-Prozess
def execute_crawling(set_id, set_name, part_crawler, mp_queue):
    """
    Führt den Crawling-Vorgang für ein LEGO-Set durch.
    :param set_id: ID des LEGO-Sets.
    :param set_name: Name des LEGO-Sets.
    :param part_crawler: Eine Instanz von PartCrawler.
    :param mp_queue: Eine Multiprocessing-Queue für die Ergebnisse.
    """
    crawler = part_crawler
    crawl_result = crawler.crawl_set_parts(set_id, set_name)

    # Platzierung der Ergebnisse in der Multiprocessing-Queue
    for i in crawl_result.stueckliste:
        mp_queue.put(i)
    mp_queue.put(None)  # Platzierung eines Platzhalters, um das Ende der Queue zu markieren

# Hauptblock des Skripts
if __name__ == "__main__":
    # Initialisierung des Loggers, Startzeit und Abrufen der ausstehenden Sets
    sl = SetLogger()
    starttime = datetime.datetime.now()
    years = ["2006", "2007", "2008", "2009", "2010"]
    for year in years:
        remaining_sets = sl.missing_set_log(year=year)
        setcount = 0

        # Schleife durch die ausstehenden Sets
        for set in remaining_sets:
            # Erstellen einer Datenzugriffsobjekt-Instanz und einer Multiprocessing-Queue
            dao = Datenzugriffsobjekt()
            mp_queue = multiprocessing.JoinableQueue()

            # Erstellen und Starten eines Prozesses für das Crawling
            p = Process(target=execute_crawling, args=(set[0], set[1], PartCrawler(), mp_queue))
            p.start()

            # Abrufen der Ergebnisse aus der Multiprocessing-Queue
            stueckliste = []
            while True:
                queue_value = mp_queue.get()
                if queue_value is None:
                    break
                else:
                    stueckliste.append(queue_value)

            p.join()  # Warten auf das Ende des Prozesses

            # Handhabung der Ergebnisse und Aktualisierung von Logger und Datenbank
            if len(stueckliste) > 0:
                sl.add_succesful_set(set[0], set[1], year)
                dao.fuge_einzelteil_legoset_hinzu(stueckliste)
            else:
                sl.add_failed_set(set[0], set[1], year)
            dao.Session.close_all()
            # Aktualisierung der Set-Zählung und Ausgabe des Fortschritts
            setcount = setcount + 1
            print(datetime.datetime.now() - starttime)
            print(f"{setcount}/{len(remaining_sets)}  {setcount * 100 / len(remaining_sets)}%")
