import datetime
from scrapy.crawler import CrawlerProcess
import os

if(os.name == 'posix'):
    from crawler.crawler import Crawler
    from crawler.teileSpider.teileSpider.spiders.lego_spider import LegoSpider
    from datastructures.crawl_result import CrawlResult
    from Entity.entities import Einzelteil, EinzelteilMarktpreis, Anbieter
    from utility.converter import preis_zu_float
else:
    from source.crawler.crawler import Crawler
    from source.crawler.teileSpider.teileSpider.spiders.lego_spider import LegoSpider
    from source.datastructures.crawl_result import CrawlResult
    from source.Entity.entities import Einzelteil, EinzelteilMarktpreis, Anbieter
    from source.utility.converter import preis_zu_float

"""API für die Lego.com Spider"""
class LegoCrawler(Crawler):
    def __init__(self):
        pass

    """startet eine Spider, welche zu einer Element Id den Preis vom Offiziellen Lego Shop abfragt. Wenn diese Methode
    angewendet muss sie in einem Prozess gestartet werden"""
    def crawl_preis(self, legoteile):
        """
        Crawlt die Preise zu einer Liste von Einzelteilen
        :param legoteile: Eine Liste von Legoeinzelteilen
        :type Legoteile: Eine Liste von Einzelteil-ID
        """

        process = CrawlerProcess()
        results = []
        # die .crawl Methode übergibt der Spider die Initialisierungsparameter, also was gecrawelt wird und wohin
        # es gespeichert wird. results ist eine Liste und hat den Aufbau (0:einzelteil, 1:preis, 2:name, 3:url)
        process.crawl(LegoSpider, legoteile=legoteile, result=results)
        process.start()

        einzelteil_marktpreise = []
        failed_einzelteile = []
        for i in results:
            if i[1] == None:
                # 1. Fall: die Element-IDs der fehlgeschlagenen Crawlvorgänge werden gespeichert
                failed_einzelteile.append(Einzelteil(einzelteil_id=i[0]))
            else:
                # 2. Fall: jeder erfolgreicher Crawlvorgang erzeugt eine neue Einzelteil_Marktpreis Entity

                einzelteil_marktpreise.append(
                    EinzelteilMarktpreis(einzelteile=Einzelteil(einzelteil_id=i[0]),
                                         preis=preis_zu_float(i[1]),
                                         url=i[3],
                                         anbieter=Anbieter(name="Lego", url="https://www.lego.com/de-de/pick-and-build/pick-a-brick")))


        crawl_result = CrawlResult(einzelteil_marktpreise,failed_einzelteile,1)
        return crawl_result