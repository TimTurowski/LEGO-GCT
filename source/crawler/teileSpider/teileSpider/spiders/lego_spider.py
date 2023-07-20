import scrapy

from source.datastructures.einzelteil import Einzelteil
from source.utility import element_id_von_url
"""Die Klasse Lego Spider ist eine Scrapy Spider, welcher die einzelteilpreise Crawlen kann"""


class LegoSpider(scrapy.Spider):
    name = "lego_spider"
    custom_settings = {
        "LOG_ENABLED": False,
    }

    """Spider wird mit den elementId der zu crawlenden Einzelteile initiiert. 
    Der Spider wird ein Set übergeben, welches die ergebnisse des Crawlers sammelt"""

    def __init__(self, legoteile, result, shop_url="https://www.lego.com/de-de/pick-and-build/pick-a-brick"):
        self.search_urls = []

        """aus die übergebenen einzelteile werden durch ein Zusammen hängen mit der Shop Url und ?query=
         eine Url generiert, welche die Suche nach einen Einzelteil wieder spiegelt"""

        # element_ids = list(map(lambda n: n.element_id, legoteile))
        element_ids = list(map(lambda n: n.einzelteil_id, legoteile))

        for i in element_ids:
            self.search_urls.append(shop_url + "?query=" + i)
        self.result = result
        self.__legoteile = legoteile

    """die generierten search_urls werden als zu crawlende Urls übergeben und der Crawl prozess wird gestartet"""

    def start_requests(self):
        urls = self.search_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    """parst die jeweiligen HTML seiten und filtert die Relevanten HTML Tags, welche im Result benötigt werden"""

    def parse(self, response):
        """Vollständige Xpath zu den jeweiligen Elementen der Html Seite"""

        preis_xpath = "/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li[1]/div/div[1]/span/span/text()"
        name_xpath = "/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li/div/button/span/text()"

        """default auf None so wird falls kein Stein zur Element ID gefunden wird None zurück in das Result 
        geschrieben"""
        preis = response.xpath(preis_xpath).get(default=None)
        name = response.xpath(name_xpath).get(default=None)

        if preis == name is None:
            """Fall das Einzelteil nicht gefunden Wird gibt Einzelteil mit None Werten zurück"""

            self.result.append((element_id_von_url(response.request.url), None, None, None))
        else:
            """Fall das gefunden Einzelteil nicht gefunden Wird"""

            self.result.append(
                (element_id_von_url(response.request.url), preis, name, response.request.url))
