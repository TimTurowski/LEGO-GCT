"""Beispiel für einen Crawlvorgang, welcher anschließend die Teile in der Datenbank speichert"""
import multiprocessing
from multiprocessing import Process

from source.Entity.entities import Einzelteil
from source.crawler import LegoCrawler
from source.datenbanklogik.datenzugriffsobjekt import marktpreis_hinzufuegen


def execute_crawling(einzelteile, teile_crawler, conn2):
    crawler = teile_crawler
    result = crawler.crawl_preis(einzelteile)
    conn2.send(result)

if __name__ == '__main__':
    sample_einzelteile = [Einzelteil(einzelteil_id="6432033"),
                          Einzelteil(einzelteil_id="6416525"),
                          Einzelteil(einzelteil_id="6411329"),
                          Einzelteil(einzelteil_id="6439666"),
                          Einzelteil(einzelteil_id="6337627")]
    conn1, conn2 = multiprocessing.Pipe()
    """erstellt Prozess in welchem der Crawl vorgang gestartet wird dies ermöglicht mehrere Crawl vorgänge"""
    p = Process(target=execute_crawling, args=(sample_einzelteile, LegoCrawler(), conn2))
    p.start()
    p.join()
    lego_crawl_result = conn1.recv()
    einzelteil_marktpreise = lego_crawl_result.einzelteil_marktpreise
    print(einzelteil_marktpreise)
    for i in einzelteil_marktpreise:
        print(i)
        marktpreis_hinzufuegen(i)
