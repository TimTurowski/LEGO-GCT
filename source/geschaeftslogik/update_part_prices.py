from multiprocessing import Process
import sys
import os
if(os.name == 'posix'):
    from crawler import LegoCrawler
    from crawler.toypro_crawler import ToyproCrawler
    from Entity.entities import Einzelteil
    from datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
else:
    from source.crawler import LegoCrawler
    from source.crawler.toypro_crawler import ToyproCrawler
    from source.Entity.entities import Einzelteil
    from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt



def execute_crawling(einzelteile, teile_crawler, anbieter):
    """Diese Funktion umfasst die Crawling-Logik
        :param einzelteile: Eine Liste mit Einzelteilen, die gecrawelt werden sollen
        :type einzelteile: Liste im Format (Einzelteil-ID)
        :param teile_crawler: Angegeben wird der Shopspezifische Crawler
        :type teile_crawler: Objekt der Klasse Crawler
        :param anbieter: Die URL des Shops, notwendig für die Zuordnung in der DB
        :type anbieter: string
        """
    crawler = teile_crawler
    # result ist ein Objekt mit einer Liste von gecrawlten Legoeinzelteilen, eine Liste von Legoeinzelteilen dessen
    # crawlvorgang nicht erfolgreich war, die Zeitangabe wie lang der Crawlvorgang gedauert hat und den Zeitstempel
    # des Crawlvorgangs
    result = crawler.crawl_preis(einzelteile)
    print(result.failed_lego_teile)
    dao = Datenzugriffsobjekt()
    # updated die Preise der erfolgreich gecrawlten Einzelteile
    dao.update_einzelteil_marktpreise(result.einzelteil_marktpreise)

    # löscht alle Marktpreise aus der DB, welche nicht mehr verfügbar sind
    print(result.failed_lego_teile)
    dao.remove_einzelteil_marktpreise(result.failed_lego_teile, anbieter)


if __name__ == "__main__":
    # setzt Defaultwerte für Crawler, falls kein Argument aufgeführt ist
    shop_url = "https://www.toypro.com"
    shop_crawler = ToyproCrawler()
    dao = Datenzugriffsobjekt()

    # wertet die Argumente aus, welcher Crawler ausgewählt ist
    if len(sys.argv) > 1:
        if sys.argv[1] == "toypro":
            shop_url = "https://www.toypro.com"
            shop_crawler = ToyproCrawler()
        elif sys.argv[1] == "lego":
            shop_url = "https://www.lego.com/de-de/pick-and-build/pick-a-brick"
            shop_crawler = LegoCrawler()


    # fragt eine Einzelteil <-> Marktpreis-Liste aus der DB ab
    marktpreise = dao.einzelteil_marktpreis_liste(shop_url)
    # mapt die obige Liste in eine Einzelteilliste
    einzelteile = list(map(lambda a: Einzelteil(einzelteil_id=a[0]), marktpreise))

    execute_crawling(einzelteile, shop_crawler, shop_url)
    # p = Process(target=execute_crawling, args=(einzelteile, shop_crawler))
    # # 6437883 0.86
    # p.start()

