import multiprocessing
from multiprocessing import Process

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

    # erstellen einer Liste von Set Ids
    ids = list(map(lambda a: a.set_id, dao.lego_set_liste()))[10:100]
    print(len(ids))
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
    dao.gib_alle
    print(einzelteil_details)
    dao.fuge_einzelteildetails_hinzu(einzelteil_details)


