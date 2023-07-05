import scrapy
from scrapy.crawler import CrawlerProcess


class LegoSpider(scrapy.Spider):
    name = "lego_spider"
    start_urls = ["https://www.lego.com/de-de/pick-and-build/pick-a-brick"]

    def parse(self, response):
        element = response.xpath("/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li[1]/div/div[1]/span/span/text()").get()
        print(element)



process = CrawlerProcess()
process.crawl(LegoSpider)
process.start()

