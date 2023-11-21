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

        process = CrawlerProcess()

        """result sammelt die gecrawlten Ergebnisse mit prozess.crawl wird der Crawlprozess initialisiert und der
        Spider werden die Initialisierungsparameter übergeben"""
        results = []
        process.crawl(LegoSpider, legoteile=legoteile, result=results)
        process.start()

        einzelteil_marktpreise = []
        failed_einzelteile = []
        for i in results:
            """Resultaufbau:(0:einzelteil, 1:preis, 2:name, 3:url)"""
            if i[1] == None:
                """Fall gescheitertes Einzelteil wird zu den failed Einzelteilen hinzugefügt"""
                failed_einzelteile.append(Einzelteil(einzelteil_id=i[0]))
            else:
                """Fall erfolgreiche Einzelteil wird als Marktwert erstellt und zu den Erfolgreichen hinzugefügt"""

                einzelteil_marktpreise.append(
                    EinzelteilMarktpreis(einzelteile=Einzelteil(einzelteil_id=i[0]),
                                         preis=preis_zu_float(i[1]),
                                         url=i[3],
                                         anbieter=Anbieter(name="Lego", url="https://www.lego.com/de-de/pick-and-build/pick-a-brick")))


        crawl_result = CrawlResult(einzelteil_marktpreise,failed_einzelteile,1)
        return crawl_result