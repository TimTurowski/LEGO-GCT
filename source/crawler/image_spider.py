import base64

import scrapy
from scrapy.crawler import CrawlerProcess


class SetImageSpider(scrapy.Spider):
    """
    Objekte dieser Klasse sind speziell für SetBilder angepasste Spider
    """
    name = "Set Image Spider"
    def __init__(self, result,set_ids):
        self.result = result
        self.set_ids = set_ids
        self.urls = list(map(lambda n: "https://www.steinelager.de/de/set/"+n+"-1", set_ids))

    def start_requests(self):
        """
        Diese Funktion sammelt bzw. bastelt alle zu parsenden URL und übergibt diese an die .parse Methode
        """
        for set_id in self.set_ids:
            yield scrapy.Request(url="https://www.steinelager.de/de/set/"+set_id+"-1", callback=self.parse,cb_kwargs={"set_id": set_id})

    def parse(self, response, set_id):
        """
        Diese Funktion parsed die URL nach dem Bild
        :param response: HTML Konstrukt der URL
        :type response: scrapy.Request
        :param set_id: Set_ID der Seite, die geparsed werden soll
        :type set_id: string
        """

        # image hat die URL zu dem zughörigen Bild
        image = response.xpath("/html/body/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/a/img/@src").get()
        yield scrapy.Request(url="https://www.steinelager.de" + image, callback=self.load_image ,cb_kwargs={"set_id": set_id})

    def load_image(self, response, set_id):
        """
        Diese Funktion lädt das Bild und codiert es in Base64
        :param response: Das HTML konstrukt, in dessen body das Bild steckt
        :type response: scrapy.Request
        :param set_id: Set_ID, dessen Bild hier extrahiert werden soll
        :type set_id: string
        """
        encoded_image = base64.b64encode(response.body)
        self.result.append((set_id, str(encoded_image)[2:][:-1]))
