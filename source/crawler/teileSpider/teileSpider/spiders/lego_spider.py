import scrapy

from source.datastructures.einzelteil import Einzelteil
from source.utility import element_id_von_url
"""Die Klasse Lego Spider ist eine Scrapy Spider, welcher die einzelteilpreise Crawlen kann"""

class LegoSpider(scrapy.Spider):
    name = "lego_spider"
    custom_settings = {
        "LOG_ENABLED": False,
    }

    """Spider wird mit den elementId der zu crawlenden Einzelteiele initiert. 
    Der Speider wird ein Set übergeben, welches die ergebnisse ders Crawlens sammelt"""
    def __init__(self, legoteile, result, shop_url ="https://www.lego.com/de-de/pick-and-build/pick-a-brick"):
        self.search_urls = []

        """aus die übergebenen einzelteile werden duch ein Zusammen hängen mit der Shop Url und ?query=
         eine Url generiert, welche die Suche nach einen Einzelteil wiederspiegelt"""

        element_ids = list(map(lambda n: n.element_id, legoteile))

        for i in element_ids:
            self.search_urls.append(shop_url + "?query=" + i)
        self.result = result
        self.__legoteile = legoteile

    """die generierten search_urls werden als zu crawlende Urls übergeben und der Crawl prozess wird gestartet"""
    def start_requests(self):
        urls = self.search_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    """parset die jeweiligen HTML seiten und filtert die Relevanten HTML Tags, welche im Result benötigt werden"""
    def parse(self, response):
        preis = response\
            .xpath("/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li[1]/div/div[1]/span/span/text()").get()
        name = response\
            .xpath("/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li/div/button/span/text()").get()

        print(name, preis)
        self.result.append((Einzelteil(element_id_von_url(response.request.url), name), preis, name, response.request.url))



