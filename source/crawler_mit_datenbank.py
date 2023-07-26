"""Beispiel für einen Crawlvorgang, welcher anschließend die Teile in der Datenbank speichert"""
import multiprocessing
from multiprocessing import Process

from source.Entity.entities import Einzelteil
from source.crawler import LegoCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt


def execute_crawling(einzelteile, teile_crawler, conn2):
    crawler = teile_crawler
    result = crawler.crawl_preis(einzelteile)
    conn2.send(result)

if __name__ == '__main__':
    sample_einzelteile = [Einzelteil(einzelteil_id="371026")]
    conn1, conn2 = multiprocessing.Pipe()
    """erstellt Prozess in welchem der Crawl vorgang gestartet wird dies ermöglicht mehrere Crawl vorgänge"""
    p = Process(target=execute_crawling, args=(sample_einzelteile, LegoCrawler(), conn2))
    p.start()
    p.join()
    lego_crawl_result = conn1.recv()
    einzelteil_marktpreise = lego_crawl_result.einzelteil_marktpreise
    dao = Datenzugriffsobjekt()
    for i in einzelteil_marktpreise:
        dao.fuge_einzelteil_marktpreis_hinzu(i)
