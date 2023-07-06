import scrapy
from scrapy.crawler import CrawlerProcess

"""Die Klasse Lego Spider ist eine Scrapy Spider, welcher die einzelteilpreise Crawlen kann"""

class LegoSpider(scrapy.Spider):
    name = "lego_spider"

    """Spider wird mit den elementId der zu crawlenden Einzelteiele initiert. 
    Der Speider wird ein Set übergeben, welches die ergebnisse ders Crawlens sammelt"""
    def __init__(self, element_ids, result, shop_url ="https://www.lego.com/de-de/pick-and-build/pick-a-brick"):
        self.search_urls = []

        """aus die übergebenen elementIds wird duch ein Zusammen hängen mit der Shop Url und ?query=
         eine Url generiert, welche die Suche nach einen Einzelteil wiederspiegelt"""
        for i in element_ids:
            self.search_urls.append(shop_url + "?query=" + i)
        self.result = result

    """die generierten search_urls werden als zu crawlende Urls übergeben und der Crawl prozess wird gestartet"""
    def start_requests(self):
        urls = self.search_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    """parset die jeweiligen HTML seiten und filtert die Relevanten HTML Tags, welche im Result benötigt werden"""
    def parse(self, response):
        element = response\
            .xpath("/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li[1]/div/div[1]/span/span/text()").get()
        self.result.add(element)



process = CrawlerProcess()
results = set()
process.crawl(LegoSpider, einzelteil_ids=["300526", "6435930"], result=results)
process.start()

for i in results:
    print(i)

