import multiprocessing
from multiprocessing import Process

from source.crawler import LegoCrawler
from source.crawler.toypro_crawler import ToyproCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
from source.utility.part_logger import PartLogger


def execute_crawling(einzelteile, teile_crawler, mp_queue):
    """diese Funktion soll alle Preise zu den übergebenen Einzelteilen crawlen.
    Übergeben werden kann sowohl der ToyPro Crawler als auch der Lego Crawler"""
    crawler = teile_crawler
    # crawlt die Preise
    result = crawler.crawl_preis(einzelteile)

    # alle erfolgreichen Elemente aus dem Crawl vorgang werden in die Queue gelegt
    for i in result.einzelteil_marktpreise:
        mp_queue.put(i)
    mp_queue.put(None)

    # alle gescheiterten Elemente aus dem Crawl vorgang werden in die Queue gelegt
    for i in result.failed_lego_teile:
        mp_queue.put(i)
    mp_queue.put(None)


if __name__ == '__main__':
    dao = Datenzugriffsobjekt()
    mp_queue = multiprocessing.JoinableQueue()

    # die Logger haben die Aufgabe mitzuschreiben, welche Teile gecrawlt worden sind und welche nicht dies ermöglicht
    # es den Crawlvorgang beim Aufbau der Bestandsdatenbank zu unterbrechen und an der unterbrochenen Stelle wieder
    # einzusteigen
    pl = PartLogger("../setIds/partIds/")
    parts = pl.missing_parts("parts", "parts_toypro_log")

    # hier können die Crawler angepasst werden der
    p = Process(target=execute_crawling, args=(parts, ToyproCrawler(), mp_queue))
    p.start()

    successful_marktpreise = []
    failed_marktpreise = []

    # es werden die erfolgreichen Marktpreise aus der Queue entgegengenommen
    while True:
        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            if queue_value.einzelteile.einzelteil_id is not None:
                successful_marktpreise.append(queue_value)

    # es werden die gescheiterten Marktpreise aus der Queue entgegengenommen
    while True:
        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            failed_marktpreise.append(queue_value)

    # fügt alle gefundenen Marktpreise in die DB hinzu
    dao.fuge_einzelteil_marktpreis_hinzu(successful_marktpreise)

    # ausgabe zur Erfolgsquote des Crawlvorgangs
    print(f"{len(successful_marktpreise) * 100 / (len(failed_marktpreise) + len(successful_marktpreise))}%")

    # loggen der Einzelteile
    pl.log_succesful_parts("parts_toypro_log", successful_marktpreise)
    pl.log_failed_parts("parts_toypro_log", failed_marktpreise)
    p.join()
