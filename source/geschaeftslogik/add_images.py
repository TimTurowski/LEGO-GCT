from source.crawler.set_crawler import SetCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt

if __name__ == "__main__":
    dao = Datenzugriffsobjekt()
    sc = SetCrawler()
    legosets = dao.lego_set_liste_ohne_bilder()
    legosetids = list(map(lambda a: a.set_id, legosets))
    crawl_result = sc.crawl_set_image(legosetids)
    for i in crawl_result:
        dao.fuge_set_bild_hinzu(i[0], i[1])