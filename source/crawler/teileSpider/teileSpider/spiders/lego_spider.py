import scrapy


class LegoSpiderSpider(scrapy.Spider):
    name = "lego_spider"
    allowed_domains = ["Lego.com"]
    start_urls = ["http://Lego.com/"]

    def parse(self, response):
        pass
