import csv
import multiprocessing
from multiprocessing import Process

from source.Entity.entities import SetMarktpreis, Anbieter
from source.crawler.set_crawler import SetCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt


def excute_crawl_setpreise(crawler, ids, mp_queue):
    prices = crawler.crawl_set_prices(ids)

    for i in prices:
        mp_queue.put(i)
    mp_queue.put(None)



if __name__ == "__main__":
    dao = Datenzugriffsobjekt()
    """Nimmt ein Intervall von SetIDs aus der Datenbank"""
    ids = list(map(lambda a:a.set_id, dao.lego_set_liste()))[4000:]

    """startet Prozess für das Crawlen von Setpreisen"""

    mp_queue = multiprocessing.JoinableQueue()

    sc = SetCrawler()
    p = Process(target=excute_crawl_setpreise, args=[sc, ids, mp_queue])
    p.start()

    set_prices = []

    while True:
        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            set_prices.append(queue_value)
    p.join()
    """holt Setpreise aus dem Prozess"""


    """Liste welche alle fertigen Entities enthalten soll."""
    marktpreis_entities = []
    for i in set_prices:
        set_price = SetMarktpreis(set= list(filter(lambda a:a.set_id == i[0],dao.lego_set_liste()))[0],
                                preis= i[1],
                                anbieter=Anbieter(name="Steinlager", url="https://www.steinelager.de/de"),
                                url= i[2])
        print(set_price)
        if set_price.preis > 0:
            marktpreis_entities.append(set_price)
    dao.fuge_set_marktpreis_hinzu(marktpreis_entities)


