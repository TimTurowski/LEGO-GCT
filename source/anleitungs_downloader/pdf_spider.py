import scrapy
from scrapy.crawler import CrawlerProcess
import os

if(os.name == 'posix'):
    from utility import set_id_von_url
    from utility import clean_setname
else:
    from source.utility import set_id_von_url
    from source.utility import clean_setname


class PdfSpider(scrapy.Spider):
    """
    Objekte dieser Klasse sind speziell für das Downloaden der Anleitungs PDF angepasste Spider
    """
    name = "pdfSpider"
    url_base = "https://www.steinelager.de/de/buildinstructions/"


    def __init__(self, set_ids, result, path_base):
        self.set_ids = set_ids
        self.result = result
        self.start_urls = list(map(lambda a: self.url_base + a + "-1?additionalManuals=0", set_ids))
        self.path_base = path_base

    def start_requests(self):
        """
        Diese Funktion startet die Reihe an Funktionsaufrufen für die PDF-Spider
        """
        # ausgehend von, in das PDFSpider Objekt, übergebenen urls wird zu jeder dieser urls die .parse() methode
        # aufgerufen
        urls = self.start_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Diese Funktion startet das parsen über die angegebene HTML Seite
        :param response: zu parsende HTML Seite
        :type response: scrapy.Request
        """
        # nimmt alle Download urls aus dem Download bereich und entfernt Duplikate
        download_urls = list(set(response.css("a::attr(href)").getall()))
        print(download_urls)
        # als Result wird ein dict übergeben, welches  den Namen des Sets beinhaltet und ob das Set eine Anleitung hat

        self.result[set_id_von_url(response.url)] = len(download_urls) > 0
        for i in download_urls:
            if i.find("Translate") == -1:
                yield scrapy.Request(url=i, callback=self.savePdf)

    def savePdf(self, response):
        """
        Diese Funktion speichert die PDFs
        :param response: zu speichernde PDF
        :type response: scrapy.Request
        """
        # Pfad zum Speichern der Dateien. Dateien werden nach der Artikelnummer der Anleitung benannt
        path = self.path_base + response.url.split('/')[-1]
        self.logger.info('PDF speichern %s', path)
        # pdf Writer wb für binary modus
        with open(path, 'wb') as writer:
            writer.write(response.body)



