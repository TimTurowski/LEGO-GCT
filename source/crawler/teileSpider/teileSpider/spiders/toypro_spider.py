import scrapy
from scrapy.crawler import CrawlerProcess

from source.datastructures.einzelteil import Einzelteil
from source.utility.validator import is_correct_toypro_element
from source.utility.converter import element_id_von_url
from source.utility.converter import preis_zu_float


class ToyproSpider(scrapy.Spider):
    name = "toypro_spider"

    def __init__(self, legoteile, result, shop_url="https://www.toypro.com/en/"):

        self.search_urls = []
        """erstellt eine Liste mit element_ids zu den Einzelteilen"""
        element_ids = list(map(lambda n: n.element_id, legoteile))
        for i in element_ids:
            """search?search= wird an die Shop Url dran gehangen, da dies eine Url für die Suche nach den 
            Einzelteilen ist"""
            self.search_urls.append(shop_url + "search?search=" + i)
        self.result = result

    def start_requests(self):
        urls = self.search_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Xpath´s zu den relevanten Html Elementen"""

        element_id_xpath = "/html/body/main/div[4]/div/div/div[1]/div/div[1]/span/text()"
        name_xpath = "/html/body/main/div[4]/div/div/div[1]/div/div[1]/span/span/text()"
        preis_xpath = "/html/body/main/div[4]/div/div/div[1]/div/div[2]/span/text()"

        """es ist sinnvoll hier die die Element Id der ToyPro Seite, auf übereinstimmung mit der gesuchten Id zu 
        prüfen. Da die Suche des Crawlers auf die Suche der Website basiert kann es sein das andere Suchergebnisse als
        die Einzelteile zur gesuchten Id angezeigt werden"""
        print(
            is_correct_toypro_element(element_id_von_url(response.request.url), response.xpath(element_id_xpath).get()))

        print(response.xpath(name_xpath).get())
        print(preis_zu_float(response.xpath(preis_xpath).get()))


process = CrawlerProcess()

"""result sammelt die gecrawlten Ergebnisse mit prozess.crawl wird der Crawl prozess initialisiert und der
Spider werden die Initialisierungsparameter übergeben"""
results = []
process.crawl(ToyproSpider, legoteile=[Einzelteil("6411329")], result=results)
process.start()
