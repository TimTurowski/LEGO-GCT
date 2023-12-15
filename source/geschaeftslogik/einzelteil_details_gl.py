import multiprocessing
from multiprocessing import Process
import os

if(os.name == 'posix'):
    from crawler.part_crawler import PartCrawler
    from datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
else:
    from source.crawler.part_crawler import PartCrawler
    from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt


def execute_crawling(set_ids, details_crawler, mp_queue):
    """funktion zum Ausführen des Crawlens in einen anderen Prozess"""

    crawler = details_crawler
    result = crawler.crawl_part_details(set_ids)

    # alle gecrawlten Details werden in eine Queue gelegt, um auf sie im Eltern Prozess zuzugreifen
    for i in result:
        mp_queue.put(i)
    # None zum Kennzeichnen das alle Elemente abgearbeitet worden sind
    mp_queue.put(None)


if __name__ == "__main__":

    # zum Zugriff auf alle Set Ids der DB
    dao = Datenzugriffsobjekt()

    mp_queue = multiprocessing.JoinableQueue()

    # erstellen einer Liste von Set Ids, die Zahl beschränkt die Sets auf alle, welche minimum von (z.b.) 5 Einzelteilen
    # ohne Details besitzen
    ids = list(map(lambda a: a[0], dao.lego_set_mit_einzelteil_ohne_einzelteildetails(5)))
    print(len(ids))
    dao.Session.close_all()
    # crawlt zu allen übergebenen Sets die Einzelteildetails
    p = Process(target=execute_crawling, args=(ids, PartCrawler(), mp_queue))

    p.start()

    einzelteil_details = []

    # Die Schleife läuft so lange bis ein None-Element in der Queue ist
    while True:
        queue_value = mp_queue.get()
        if queue_value is None:
            #None ist die Abbruch bedingung
            break
        else:
            einzelteil_details.append(queue_value)
    dao = Datenzugriffsobjekt()
    dao.fuge_einzelteildetails_hinzu(einzelteil_details)