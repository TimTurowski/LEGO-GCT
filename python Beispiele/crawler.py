from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process


class LegoShopSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        "USER_AGENT": 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    }

    def __init__(self, shop_url, element_id, result):
        # self.search_url = shop_url +"?query=" + element_id
        self.search_url = "https://www.steinelager.de/img/sets/1/0/3/1/2/10312-1_0-lg.jpg"
        self.result = result

    def start_requests(self):

        urls = [self.search_url]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        print(response.body)
        path = response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)
        # print(response.css('[class = "set"]').css("a::text").getall())

        # for i in response.css('[class = "set"]').css("a > span::text").getall():
        #     print(i.lower())







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
    process = CrawlerProcess()
    process.crawl(LegoShopSpider, shop_url="https://www.lego.com/de-de/pick-and-build/pick-a-brick",
                  element_id="6359941", result=results)
    process.start()
    for i in results:
        print(i)

if __name__ == '__main__':

    for k in range(0,1):
        p = Process(target=execute_crawling)
        p.start()
        p.join()

