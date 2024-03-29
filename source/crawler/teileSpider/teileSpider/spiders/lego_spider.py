import scrapy
import os

if (os.name == 'posix'):
    from utility import element_id_von_url
else:
    from source.utility import element_id_von_url


class LegoSpider(scrapy.Spider):
    """Die Klasse Lego Spider ist eine Scrapy Spider, welcher die Einzelteilpreise Crawlen kann"""

    name = "lego_spider"
    custom_settings = {
        "LOG_ENABLED": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    def __init__(self, legoteile, result, shop_url="https://www.lego.com/de-de/pick-and-build/pick-a-brick"):
        """Spider wird mit den elementId der zu crawlenden Einzelteile initiiert.
            Der Spider wird ein Set übergeben, welches die ergebnisse des Crawlers sammelt"""
        self.search_urls = []

        # erstellen einer Liste von einzelteil Ids
        element_ids = list(map(lambda n: n.einzelteil_id, legoteile))

        for i in element_ids:
            # füllt eine die Liste search_urls mit den URLs der zu crawlenden Einzelteile
            self.search_urls.append(shop_url + "?query=" + i)
        self.result = result
        self.__legoteile = legoteile



    def start_requests(self):
        """
        Die generierten search_urls werden als zu crawlende Urls übergeben und der Crawl Prozess wird gestartet
        """
        urls = self.search_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # parst die jeweiligen HTML seiten und filtert die relevanten HTML-Tags, welche im Result benötigt werden

    def parse(self, response):
        """
        Diese Funktion parsed den Xpath der HTML Seite zu den Elementen die wir haben wollen
        :param response: Der HTML Outline der gecrawleten Seite
        """

        # Vollständige Xpath zu den jeweiligen Elementen der Html Seite
        preis_xpath = "/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li[1]/div/div[1]/span/span/text()"
        name_xpath = "/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li/div/button/span/text()"

        # default auf None so wird, falls kein Stein zur Element-ID gefunden wird None zurück in das Result geschrieben
        preis = response.xpath(preis_xpath).get(default=None)
        name = response.xpath(name_xpath).get(default=None)

        if preis == name is None:
            # 1. Fall: das Einzelteil wird nicht gefunden"""

            self.result.append((element_id_von_url(response.request.url), None, None, None))
        else:
            # 2. Fall: das Einzelteil wird gefunden

            self.result.append(
                (element_id_von_url(response.request.url), preis, name, response.request.url))
