from multiprocessing import Process
import sys

from source.crawler import LegoCrawler
from source.crawler.toypro_crawler import ToyproCrawler
from source.Entity.entities import Einzelteil
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt

"""funktion zum Ausführen der Crawling logik"""
def execute_crawling(einzelteile, teile_crawler):
    crawler = teile_crawler
    result = crawler.crawl_preis(einzelteile)
    print(result.failed_lego_teile)
    dao = Datenzugriffsobjekt()
    """updated die Preise der erfolgreich gecrawlten Einzelteile"""
    dao.update_einzelteil_marktpreise(result.einzelteil_marktpreise)

    """löscht alle Marktpreise aus der DB, welche nicht mehr verfügbar sind"""
    print(result.failed_lego_teile)
    dao.remove_einzelteil_marktpreise(result.failed_lego_teile, "https://www.toypro.com")


if __name__ == "__main__":
    dao = Datenzugriffsobjekt()

    print(len(dao.einzelteil_ohne_marktpreis("https://www.toypro.com")))




    marktpreise = dao.einzelteil_marktpreis_liste("https://www.toypro.com")[0:10]

    einzelteile = list(map(lambda a: Einzelteil(einzelteil_id=a[0]), marktpreise))

    print(len(einzelteile))
    p = Process(target=execute_crawling, args=(einzelteile, ToyproCrawler()))
    # # 6437883 0.86
    p.start()

