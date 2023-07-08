from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process


class LegoShopSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, shop_url, element_id, result):
        self.search_url = shop_url +"?query=" + element_id
        self.result = result

    def start_requests(self):

        urls = [self.search_url]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        element = response.xpath("/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li/div/button/span/text()").get() \
                  + " " + response.xpath("/html/body/div[1]/div/main/div[1]/div[6]/div[3]/div/div/ul/li/div/div[1]/span/span/text()").get()
        self.result.append(element)

        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    }
)
# process = CrawlerProcess()
# results = []
# process.crawl(LegoShopSpider,shop_url="https://www.lego.com/de-de/pick-and-build/pick-a-brick", element_id="6359941", result=results)
# process.start()
# process.join()


"""ermöglicht es mehrere Crallvorgänge zu starten"""
def execute_crawling():
    results = []
    process = CrawlerProcess()  # same way can be done for Crawlrunner
    process.crawl(LegoShopSpider, shop_url="https://www.lego.com/de-de/pick-and-build/pick-a-brick",
                  element_id="6359941", result=results)
    process.start()
    for i in results:
        print(i)

if __name__ == '__main__':

    for k in range(0,3):
        p = Process(target=execute_crawling)
        p.start()
        p.join()

