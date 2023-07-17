import scrapy
from scrapy.crawler import CrawlerProcess


class PdfSpider(scrapy.Spider):
    name ="pdfSpider"

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""
        urls = ["https://www.steinelager.de/de/set/79015-1"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """soll alle Download Links auslesen und Pdf herunterladen"""
        download =response.xpath(
            "/html/body/div/div[2]/div/div/div[2]/div/div[2]/div[5]/div/div[2]/div/div/div[1]/div/div[3]/div/div/a").attrib["href"]
        yield scrapy.Request(url=download, callback=self.savePdf)



    def savePdf(self, response):
        """pfad zum Speichern der Datei"""
        path = response.url.split('/')[-1]
        self.logger.info('PDF speichern %s', path)
        """pdf Writer wb für binary modus"""
        with open(path, 'wb') as writer:
            writer.write(response.body)




process = CrawlerProcess()
process.crawl(PdfSpider)
process.start()