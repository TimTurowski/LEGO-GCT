import scrapy
from scrapy.crawler import CrawlerProcess


class PdfSpider(scrapy.Spider):
    name ="pdfSpider"

    def start_requests(self):

        urls = ["https://www.lego.com/cdn/product-assets/product.bi.core.pdf/6360713.pdf"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        """pdf Writer wb für binary modus"""
        with open(path, 'wb') as f:
            f.write(response.body)




process = CrawlerProcess()
process.crawl(PdfSpider)
process.start()