import scrapy
import os

if(os.name == 'posix'):
    from utility.validator import is_correct_toypro_element
    from utility.converter import element_id_von_url
else:
    from source.utility.validator import is_correct_toypro_element
    from source.utility.converter import element_id_von_url


class ToyproSpider(scrapy.Spider):
    """Die Klasse ToyproSpider ist eine Scrapy Spider, welcher die Einzelteilpreise Crawlen kann"""
    name = "toypro_spider"

    custom_settings = {
        "LOG_ENABLED": True,
        "DOWNLOAD_DELAY": 0.25,
    }

    def __init__(self, legoteile, result, shop_url="https://www.toypro.com/en/"):
        """
        Spider wird mit den elementId der zu crawlenden Einzelteile initiiert.
        Der Spider wird ein Set übergeben, welches die ergebnisse des Crawlers sammelt
        """
        self.search_urls = []
        # erstellt eine Liste mit element_ids zu den Einzelteilen
        element_ids = list(map(lambda n: n.einzelteil_id, legoteile))
        for i in element_ids:
            # search?search= wird an die Shop Url dran gehangen, da dies eine Url für die Suche nach den
            # Einzelteilen ist
            self.search_urls.append(shop_url + "search?search=" + i)
        self.result = result

    def start_requests(self):
        """
        Die generierten search_urls werden als zu crawlende Urls übergeben und der Crawl Prozess wird gestartet
        """
        urls = self.search_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Diese Funktion parsed den Xpath der HTML Seite zu den Elementen die wir haben wollen
        :param response: Der HTML Outline der gecrawleten Seite
        """

        # Xpath´s zu den relevanten Html Elementen
        element_id_xpath = "/html/body/main/div[4]/div/div/div[1]/div/div[1]/span/text()"
        name_xpath = "/html/body/main/div[4]/div/div/div[1]/div/div[1]/span/span/text()"
        preis_xpath = "/html/body/main/div[4]/div/div/div[1]/div/div[2]/span/text()"

        # Es ist sinnvoll hier die die Element Id der ToyPro Seite, auf übereinstimmung mit der gesuchten Id zu
        # prüfen. Da die Suche des Crawlers auf die Suche der Website basiert kann es sein das andere Suchergebnisse als
        # die Einzelteile zur gesuchten Id angezeigt werden

        raw_element_id = response.xpath(element_id_xpath).get(default=None)
        preis = response.xpath(preis_xpath).get(default=None)
        name = response.xpath(name_xpath).get(default=None)

        if raw_element_id is not None and is_correct_toypro_element(element_id_von_url(response.request.url),
                                                                    raw_element_id):
            self.result.append((element_id_von_url(response.request.url), preis, name, response.request.url))
        else:
            self.result.append((element_id_von_url(response.request.url), None, None, None))
