import base64

import scrapy
from scrapy.crawler import CrawlerProcess


class SetImageSpider(scrapy.Spider):
    name = "Set Image Spider"
    def __init__(self, result,set_ids):
        self.result = result
        self.set_ids = set_ids
        self.urls = list(map(lambda n: "https://www.steinelager.de/de/set/"+n+"-1", set_ids))

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""
        for set_id in self.set_ids:
            yield scrapy.Request(url="https://www.steinelager.de/de/set/"+set_id+"-1", callback=self.parse,cb_kwargs={"set_id": set_id})

    def parse(self, response, set_id):


        """image hat die URL zu dem zughörigen Bild"""
        image = response.xpath("/html/body/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div/div[1]/a/img/@src").get()
        yield scrapy.Request(url="https://www.steinelager.de" + image, callback=self.load_image ,cb_kwargs={"set_id": set_id})

    def load_image(self, response, set_id):
        """läd das Bild und codiert es in Base64"""
        encoded_image = base64.b64encode(response.body)
        self.result.append((set_id, str(encoded_image)[2:][:-1]))
