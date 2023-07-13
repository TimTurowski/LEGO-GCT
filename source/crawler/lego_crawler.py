import datetime

from source.crawler.crawler import Crawler
from source.crawler.teileSpider.teileSpider.spiders import LegoSpider
from source.datastructures.crawl_result import CrawlResult
from scrapy.crawler import CrawlerProcess
from source.datastructures.einzelteil import Einzelteil
from source.datastructures.einzelteil_marktpreis import EinzelTeilMarktpreis
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

        einzelteil_markrpreise = []
        failed_einzelteile = []
        for i in results:
            """Resultaufbau:(0:einzelteil, 1:preis, 2:name, 3:url)"""
            if i[1] == None:
                """Fall gescheitertes Einzelteil wird zu den failed Einzelteilen hinzugefügt"""
                failed_einzelteile.append(i[0])
            else:
                """Fall erfolgreiche Einzelteil wird als Marktwert erstellt und zu den Erfolgreichen hinzugefügt"""
                einzelteil_markrpreise.append(EinzelTeilMarktpreis(i[0], preis_zu_float(i[1]), datetime.datetime.now(),i[3]))

        crawl_result = CrawlResult(einzelteil_markrpreise,failed_einzelteile,1)
        return crawl_result


