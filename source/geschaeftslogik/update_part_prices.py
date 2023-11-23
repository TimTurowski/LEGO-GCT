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


"""funktion zum Ausführen der Crawling logik"""
def execute_crawling(einzelteile, teile_crawler, anbieter):
    crawler = teile_crawler
    result = crawler.crawl_preis(einzelteile)
    print(result.failed_lego_teile)
    dao = Datenzugriffsobjekt()
    """updated die Preise der erfolgreich gecrawlten Einzelteile"""
    dao.update_einzelteil_marktpreise(result.einzelteil_marktpreise)

    """löscht alle Marktpreise aus der DB, welche nicht mehr verfügbar sind"""
    print(result.failed_lego_teile)
    dao.remove_einzelteil_marktpreise(result.failed_lego_teile, anbieter)


if __name__ == "__main__":
    """Defaultwerte für Crawler"""
    shop_url = "https://www.toypro.com"
    shop_crawler = ToyproCrawler()
    dao = Datenzugriffsobjekt()


    if len(sys.argv) > 1:
        if sys.argv[1] == "toypro":
            shop_url = "https://www.toypro.com"
            shop_crawler = ToyproCrawler()
        elif sys.argv[1] == "lego":
            shop_url = "https://www.lego.com/de-de/pick-and-build/pick-a-brick"
            shop_crawler = LegoCrawler()



    marktpreise = dao.einzelteil_marktpreis_liste(shop_url)

    einzelteile = list(map(lambda a: Einzelteil(einzelteil_id=a[0]), marktpreise))

    execute_crawling(einzelteile, shop_crawler, shop_url)
    # p = Process(target=execute_crawling, args=(einzelteile, shop_crawler))
    # # 6437883 0.86
    # p.start()

