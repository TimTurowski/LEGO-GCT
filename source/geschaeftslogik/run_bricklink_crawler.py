import multiprocessing
from multiprocessing import Process
import os

if(os.name == 'posix'):
    from crawler.part_crawler import PartCrawler
    from datastructures.bricklink_einzelteil import BricklinkEinzelteil
    from crawler.bricklink_crawler import BricklinkCrawler
    from datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
else:
    from source.crawler.part_crawler import PartCrawler
    from source.datastructures.bricklink_einzelteil import BricklinkEinzelteil
    from source.crawler.bricklink_crawler import BricklinkCrawler
    from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt



def execute_bricklink_crawling(mp_queue, shop_url, shop_name):
    """Diese Funktion führt einen Crawlvorgang bei Bricklink aus
        :param mp_queue: Queue, die Bricklinkergebnisse entgegen nimmt.
        :type mp_queue: multiprocessing Queue
        :param shop_url: url des zu crawlenden Shops.
        :type shop_url: string
        :param shop_name: name des zu crawlenden Shops.
        :type shop_url: string
    """

    bricklink_crawler = BricklinkCrawler()
    result = bricklink_crawler.crawl(shop_url,shop_name, None)

    print(result)
    # Legt alle Objekte in der Queue ab um im Hauptprozess drauf zuzugreifen
    for i in result:
        mp_queue.put(i)
    mp_queue.put(None)




def execute_id_translation(crawl_result, shop_url, shop_name, mp_queue):
    """funktion zur übersetzung der Bricklink Id in Lego element Id
        :param crawl_result: liste von Bricklink einzelteilen.
        :type mp_queue: list of BricklinkEinzelteil
        :param shop_url: url des zu crawlenden Shops.
        :type shop_url: string
        :param shop_name: name des zu crawlenden Shops.
        :type shop_url: string
        :param mp_queue: Queue, die Bricklinkergebnisse entgegen nimmt.
        :type mp_queue: multiprocessing Queue"""

    part_crawler = PartCrawler()
    result = part_crawler.crawl_design_ids(crawl_result, shop_url, shop_name)
    print(result)
    print(len(result))

    # Multiprozessing Queue zum übertragen der Marktpreise in den Hauptprozess
    for i in result:
        mp_queue.put(i)
    mp_queue.put(None)


if __name__ == '__main__':
    # Attribute für den Bricklink shop
    shop_url = "https://store.bricklink.com/anguray#/shop?o={%22itemType%22:%22P%22,%22catID%22:%2293%22,%22invNew%22:%22N%22,%22showHomeItems%22:0}"
    shop_name = "Bricklink(Lucky-Bricks)"

    # Prozess für den Bricklink Crawlvorgang mit Selenium
    mp_queue = multiprocessing.JoinableQueue()
    p = Process(target=execute_bricklink_crawling, args=[mp_queue, shop_url, shop_name])
    p.start()

    # While Schleife wird abgebrochen, wenn alle Objekte aus der Queue genommen sind
    raw_results = []
    while True:

        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            raw_results.append(queue_value)
            print(queue_value)

    results = []

    # Datenstruktur zur Verwaltung der Desing Id und Farbcode wird aufgebaut
    for i in raw_results:
        # prüfe, ob die Design Id bereits in der Liste ist
        filtered = list(filter(lambda a: a.design_id == i[0], results))
        if len(filtered) == 0:
            # fügt neues BricklinkEinzelteil in die Liste, da zur gegebenen Design Id noch kein Element vorhanden ist
            results.append(BricklinkEinzelteil(i[0], i[1].rstrip(), i[2]))
        else:
            # fügt zur existierenden Design Id eine weitere Farbe mit preis hinzu
            filtered[0].add_color(i[1].rstrip(), i[2])

    # Prozess zum starten der Übersetzung
    mp_queue = multiprocessing.JoinableQueue()
    p = Process(target=execute_id_translation, args=[results, shop_name, shop_url, mp_queue])
    p.start()

    marktpreise = []
    # annehmen der Elemente der Queue
    while True:
        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            marktpreise.append(queue_value)

    # Marktpreise in die Datenbank ablegen
    dao = Datenzugriffsobjekt()

    dao.update_einzelteil_marktpreise(marktpreise)
