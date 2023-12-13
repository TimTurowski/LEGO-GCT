import os

if(os.name == 'posix'):
    from crawler.set_crawler import SetCrawler
    from datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
else:
    from source.crawler.set_crawler import SetCrawler
    from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt

if __name__ == "__main__":
    """Es soll zu jeder vorhandenen Set-Id das entsprechende Bild hinzugefügt werden"""

    dao = Datenzugriffsobjekt()
    sc = SetCrawler()

    # alle Lego Sets, welche kein Bild haben
    lego_sets = dao.lego_set_liste_ohne_bilder()

    # erstellt eine Liste an Set Ids
    lego_set_ids = list(map(lambda a: a.set_id, lego_sets))

    # crawlt alle Bilder un kodiert sie in Base64
    crawl_result = sc.crawl_set_image(lego_set_ids)

    # alle Bilder werden der DB hinzugefügt
    for i in crawl_result:
        dao.fuge_set_bild_hinzu(i[0], i[1])