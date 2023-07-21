import scrapy
from scrapy.crawler import CrawlerProcess
from source.utility import set_id_von_url
from source.utility import clean_setname


class PdfSpider(scrapy.Spider):
    name = "pdfSpider"
    url_base = "https://www.steinelager.de/de/set/"

    def __init__(self, set_ids, result, path_base):
        self.set_ids = set_ids
        self.result = result
        self.start_urls = list(map(lambda a: self.url_base + a + "-1", set_ids))
        self.path_base = path_base

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""
        urls = self.start_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        download_xpath = "/html/body/div/div[2]/div/div/div[2]/div/div[2]/div[5]/div/div[2]/div/div/div[1]/div/div[3]"
        """soll alle Download Links auslesen und Pdf herunterladen"""
        setname = response.css("h1::text").get(default=None)

        if setname is None:
            self.result[set_id_von_url(response.url)] = None

        else:

            """nimmt alle Download urls aus dem Download bereich und entfernt Duplikate"""
            download_urls = list(set(response.xpath(download_xpath).css("a::attr(href)").getall()))
            """als Result wird ein dict übergeben, welches  den Namen des Sets beinhaltet und ob das Set eine Anleitung hat"""
            self.result[set_id_von_url(response.url)] = (clean_setname(setname), len(download_urls) > 0)

            for i in download_urls:
                yield scrapy.Request(url=i, callback=self.savePdf)

    def savePdf(self, response):

        """pfad zum Speichern der Dateien. Dateien werden nach der Artikelnummer der Anleitung bennant"""
        path = self.path_base + response.url.split('/')[-1]
        self.logger.info('PDF speichern %s', path)
        """pdf Writer wb für binary modus"""
        with open(path, 'wb') as writer:
            writer.write(response.body)



