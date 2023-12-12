import scrapy
from scrapy.crawler import CrawlerProcess
import os
if(os.name == 'posix'):
    from utility.converter import clean_set_id
    from utility.validator import set_id_filter
else:
    from source.utility.converter import clean_set_id
    from source.utility.validator import set_id_filter

class SetSpider(scrapy.Spider):
    """
    Objekte dieser Klasse sind speziell für Suche nach Sets angepasste Spider
    """
    name = "Set Spider"
    def __init__(self, url, result):
        self.start_url = url
        self.result = result

    def start_requests(self):
        """
        Diese Funktion sammelt bzw. bastelt alle zu parsenden URL und übergibt diese an die .parse Methode
        """
        url = self.start_url
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Diese Funktion parsed das HTML Konstrukt der URL nach dem Details zu den Sets
        :param response: HTML Konstrukt der URL
        :type response: scrapy.Request
        """
        elemente = response.css("[data-key]")
        for element in elemente:
            set_id = clean_set_id(element.xpath("div/div/div/div/text()").get())
            set_name = element.css('[class="text-center text-truncate"]::text').get().strip()
            if set_id_filter(set_id):
                self.result.append((set_id, set_name))
        # untersucht aktuelle Seite ob weitere Seiten existieren, die geparsed werden müssen
        next_url = response.css('[class="next"]').css("a::attr(href)").get()
        if next_url is None:
            pass
        else:
            yield scrapy.Request(url="https://www.steinelager.de" + next_url, callback=self.parse)
