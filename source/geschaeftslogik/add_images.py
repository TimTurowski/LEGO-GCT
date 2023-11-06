from source.crawler.set_crawler import SetCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt

if __name__ == "__main__":
    sc = SetCrawler()

    crawl_result = sc.crawl_set_image(["40268"])[0]
    dao = Datenzugriffsobjekt()
    print(crawl_result[1])
    dao.fuge_set_bild_hinzu(crawl_result[0], crawl_result[1])