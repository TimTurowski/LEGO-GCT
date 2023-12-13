import multiprocessing
import sys
from multiprocessing import Process

from source.crawler import LegoCrawler
from source.crawler.toypro_crawler import ToyproCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt


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

    # wertet die Argumente aus, welcher Crawler ausgewählt ist
    if len(sys.argv) > 1:
        if sys.argv[1] == "toypro":
            shop_url = "https://www.toypro.com"
            shop_crawler = ToyproCrawler()
        elif sys.argv[1] == "lego":
            shop_url = "https://www.lego.com/de-de/pick-and-build/pick-a-brick"
            shop_crawler = LegoCrawler()
    else:
        shop_url = "https://www.toypro.com"
        shop_crawler = ToyproCrawler()

    dao = Datenzugriffsobjekt()

    mp_queue = multiprocessing.JoinableQueue()

    # parts enthält alle einzelteile, welche keinen Marktpreis haben
    # es ist durchaus sinnvoll in den Klammern eine Rangfe anzugeben [von:bis]
    parts = dao.einzelteil_ohne_marktpreis(shop_url)

    # hier können die Crawler angepasst werden der
    p = Process(target=execute_crawling, args=(parts, shop_crawler, mp_queue))
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


