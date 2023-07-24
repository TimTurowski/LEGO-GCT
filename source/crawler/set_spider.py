import scrapy
from scrapy.crawler import CrawlerProcess
from source.utility.converter import clean_set_id
from source.utility.validator import set_id_filter

class SetSpider(scrapy.Spider):
    name = "Set Spider"
    def __init__(self, url, result):
        self.start_url = url
        self.result = result

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""
        url = self.start_url
        yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        elemente = response.css("[data-key]")
        for element in elemente:
            set_id = clean_set_id(element.xpath("div/div/div/div/text()").get())
            set_name = element.css('[class="text-center text-truncate"]::text').get().strip()
            if set_id_filter(set_id):
                self.result.append((set_id, set_name))
                # print("id: " + set_id + " name: " + set_name)
        next_url = response.css('[class="next"]').css("a::attr(href)").get()
        if next_url is None:
            pass
        else:
            yield scrapy.Request(url="https://www.steinelager.de" + next_url, callback=self.parse)
