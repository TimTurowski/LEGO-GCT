import datetime

from scrapy.crawler import CrawlerProcess

from source.crawler.crawler import Crawler
from source.crawler.teileSpider.teileSpider.spiders.toypro_spider import ToyproSpider
from source.datastructures import CrawlResult
from source.datastructures.einzelteil_marktpreis import EinzelTeilMarktpreis
from source.utility import preis_zu_float


class ToyproCrawler(Crawler):
    def __init__(self):
        pass

    def crawl_preis(self, legoteile):

        process = CrawlerProcess()

        """result sammelt die gecrawlten Ergebnisse mit prozess.crawl wird der Crawl prozess initialisiert und der
        Spider werden die Initialisierungsparameter übergeben"""
        results = []
        process.crawl(ToyproSpider, legoteile=legoteile, result=results)
        process.start()
        einzelteil_marktpreise = []
        failed_einzelteile = []
        for i in results:
            """Realtaufbau:(0:einzelteil, 1:preis, 2:name, 3:url)"""
            if i[1] is None:
                """Fall gescheitertes Einzelteil wird zu den failed Einzelteilen hinzugefügt"""
                failed_einzelteile.append(i[0])
            else:
                """Fall erfolgreiche Einzelteil wird als Marktwert erstellt und zu den Erfolgreichen hinzugefügt"""
                einzelteil_marktpreise.append(
                    EinzelTeilMarktpreis(i[0], preis_zu_float(i[1]), datetime.datetime.now(), i[3]))

        crawl_result = CrawlResult(einzelteil_marktpreise, failed_einzelteile, 1)
        return crawl_result
