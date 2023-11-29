import scrapy
from scrapy.crawler import CrawlerProcess


class PartDetailsSpider(scrapy.Spider):
    name = "Part Details Spider"
    custom_settings = {
        "USER_AGENT": 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        "LOG_ENABLED": True,
        "DOWNLOAD_DELAY": 0.5,
    }
    def __init__(self, url, ids, result):
        self.base_url = url
        self.ids = ids
        self.result = result

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""

        # erstellt eine Liste mit Urls zu den Einzelteil übersichten
        urls = list(map(lambda a: self.base_url + a + "-1", self.ids))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Methode zum Parsen der Teile Liste"""

        # itteriert über alle Article Elemente mit Klasse set
        for i in response.css(".set"):

            # element id des Einzelteils
            id = i.css(".tags").css("a::text").get()

            # brickset Namensbezeichnung des Teils
            name = i.xpath("div[3]/h1/a/text()").get()

            # kategorie des Einzelteils
            categorie = i.css(".subtheme::text").getall()[1]

            #
            color = i.xpath("div[3]/div[1]/a[6]/text()").get()

            # fügt die Informationen nur hinzu wenn der Name aufgelöst werden kann
            if name is not None:

                raw_details = (id, name, categorie, color)
                self.result.add(raw_details)

        next_url = response.css(".next").css("a::attr(href)").get()
        if next_url is None:
            # alle Seiten geparst
            pass
        else:
            # nächste Seite
            yield scrapy.Request(url=next_url, callback=self.parse)



