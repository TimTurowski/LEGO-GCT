import scrapy


class ToyproSpider(scrapy.Spider):
    name = "toypro"
    allowed_domains = ["toypro.com"]
    start_urls = ["http://toypro.com/"]

    def parse(self, response):
        pass
