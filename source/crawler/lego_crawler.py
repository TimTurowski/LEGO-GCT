from crawler import Crawler
from teileSpider.teileSpider.spiders import LegoSpider
from source.datastructures.crawl_result import CrawlResult
from scrapy.crawler import CrawlerProcess
from  source.datastructures.einzelteil import Einzelteil


"""API für die Lego.com Spider"""
class LegoCrawler(Crawler):
    def __init__(self):
        pass

    """startet eine Spider, welche zu einer Element Id den Preis vom Offiziellen Lego Shop abfragt"""
    def crawl_preis(self, legoteile):

        element_ids = list(map(lambda n: n.element_id, legoteile))
        process = CrawlerProcess()

        """result sammelt die gecrawlten Ergebnisse mit prozess.crawl wird der Crawlprozess initialisiert und der
        Spider werden die Initialisierungsparameter übergeben"""
        results = []
        process.crawl(LegoSpider, element_ids=element_ids, result=results)
        process.start()

        for i in results:
             print(i[0])



a = LegoCrawler()
a.crawl_preis([Einzelteil("300526"),
               Einzelteil("6438899"),
               Einzelteil("6359941"),
               Einzelteil("6435930"),
               Einzelteil("6337627"),
               Einzelteil("6439666"),
               Einzelteil("6416525"),
               Einzelteil("6360331"),
               Einzelteil("6409580"),
               Einzelteil("6409509"),
               Einzelteil("6409588"),
               Einzelteil("6448394"),
               Einzelteil("6438899")])
