import multiprocessing
from multiprocessing import Process

from source.crawler.part_crawler import PartCrawler
from source.datastructures.bricklink_einzelteil import BricklinkEinzelteil
from source.crawler.bricklink_crawler import BricklinkCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt

"""Funktion zur Ausführung des Crawlvorgangs wird in einen anderen Prozess gestartet"""


def execute_bricklink_crawling(mp_queue, shop_url, shop_name):
    """Bricklinkcrawler zum crawlen der Bricklink seite"""
    bricklink_crawler = BricklinkCrawler()
    result = bricklink_crawler.crawl(
        shop_url,
        shop_name,
        [0,3])

    print(result)
    """Legt alle Objekte in der Queue ab um im Hauptprozess drauf zuzugreifen"""
    for i in result:
        mp_queue.put(i)
    mp_queue.put(None)


"""funktion zur übersetzung der Bricklink Id in Lego element Id"""


def execute_id_translation(crawl_result, shop_url, shop_name, mp_queue):
    part_crawler = PartCrawler()
    result = part_crawler.crawl_design_ids(crawl_result, shop_url, shop_name)
    print(result)
    print(len(result))

    """Multiprozessing Queue zum übertragen der Marktpreise in den Hauptprozess"""
    for i in result:
        mp_queue.put(i)
    mp_queue.put(None)


if __name__ == '__main__':

    shop_url = "https://store.bricklink.com/anguray#/shop?o={%22itemType%22:%22P%22,%22catID%22:%2293%22,%22invNew%22:%22N%22,%22showHomeItems%22:0}"
    shop_name = "Bricklink(Lucky-Bricks)"

    """Prozess für den Bricklink Crawlvorgang mit Selenium"""
    mp_queue = multiprocessing.JoinableQueue()
    p = Process(target=execute_bricklink_crawling, args=[mp_queue, shop_url, shop_name])
    p.start()

    """While Schleife wird abgebrochen wenn alle Objekte aus der Que genommen sind"""
    raw_results = []
    while True:

        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            raw_results.append(queue_value)
            print(queue_value)

    results = []

    """Datenstrucktur zur Verwaltung der Desing Id und Farbcode wird aufgebaut"""
    for i in raw_results:
        filtered = list(filter(lambda a: a.design_id == i[0], results))
        if len(filtered) == 0:
            results.append(BricklinkEinzelteil(i[0], i[1].rstrip(), i[2]))
        else:
            filtered[0].add_color(i[1].rstrip(), i[2])

    """Prozess zum starten der Übersetzung"""

    mp_queue = multiprocessing.JoinableQueue()
    p = Process(target=execute_id_translation, args=[results, shop_name, shop_url, mp_queue])
    p.start()

    marktpreise = []
    """annehmen der Elemente der Queue"""
    while True:
        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            marktpreise.append(queue_value)

    """Marktpreise in die Datenbank ablegen"""
    dao = Datenzugriffsobjekt()

    # dao.fuge_einzelteil_marktpreis_hinzu(marktpreise)
