import scrapy
from scrapy.crawler import CrawlerProcess


class SetPriceSpider(scrapy.Spider):
    """
    Objekte dieser Klasse sind speziell für das Crawlen von SetPreisen konfigurierte Spider
    """
    name = "Set Price Spider"
    def __init__(self, set_ids, result):
        self.urls = list(map(lambda n: "https://www.steinelager.de/de/set/"+n+"-1", set_ids))
        self.result = result

    def start_requests(self):
        """
        Diese Funktion sammelt bzw. bastelt alle zu parsenden URL und übergibt diese an die .parse Methode
        """
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Diese Funktion parsed das HTML-Konstrukt nach dem SetPreis
        :param response: HTML Konstrukt der URL
        :type response: scrapy.Request
        """
        # Preis aus xpath extrahieren
        raw_price = response.xpath("/html/body/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div/div[2]/div/div/div[2]/div/div[2]/b/text()").get()

        raw_id = response.xpath("/html/body/div/div[2]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div[2]/text()").get()

        self.result.append((raw_id[0:len(raw_id)-2], float(raw_price.replace("€", "")), response.request.url))