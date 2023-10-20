import datetime
from scrapy.crawler import CrawlerProcess
import csv

from unidecode import unidecode

from source.crawler.set_price_spider import SetPriceSpider
from source.crawler.set_spider import SetSpider
from source.utility.set_logger import SetLogger

"""Der SetCrawler kann zu einen als Parameter übergebenen Jahr alle Setids aus dem Jahr finden"""
class SetCrawler:
    """als Parameter kann ein Jahr übergeben werden zu diesem eine Liste von Sets zurück gegeben wird mit Name und ID"""
    def crawl_set_ids(self, year):
        process = CrawlerProcess()
        result = []
        process.crawl(SetSpider, url="https://www.steinelager.de/de/sets/year/" + year +"/1", result=result)
        process.start()
        self.save_as_csv(result, year)

    """Crawlt alle Sets, welche noch nicht veröffentlicht worden sind"""
    def crawl_unreleased_sets(self):
        process = CrawlerProcess()
        result = []
        year = str(datetime.datetime.now().year)
        process.crawl(SetSpider, url="https://www.steinelager.de/de/sets/year/" + year + "/1", result=result)
        process.start()

        sl = SetLogger()

        """oldset hat alle Sets die bereits in der DB sind oder keine Anleitung haben aus dem aktuellen jahr"""

        old_sets = sl.succesful_set_log(year) + sl.failed_set_log(year)
        old_sets = list(map(lambda a: (a[0], a[1]), old_sets))


        result = list(map(lambda a: (a[0], a[1].replace("\xa0", " ").replace("\u200b", "")), result))

        new_sets = list(set(result) - set(old_sets))



        """CSV Datei wird im Fromat DDMMYY gespeichert"""
        # date = datetime.datetime.now()
        # self.save_as_csv(result, date.strftime("%d") + date.strftime("%m") + date.strftime("%y"))
        return new_sets

    def crawl_set_prices(self, set_ids):
        process = CrawlerProcess()
        results = [];
        process.crawl(SetPriceSpider, set_ids=set_ids, result=results)
        process.start()
        print(results)

    """speichert das Result als eine CSV Datei"""
    def save_as_csv(self, result, name):
        """Gecrawlte Sets werden als SetId mit Namen in eine CSV Datei geschrieben"""
        with open("../setIds/" + name + ".csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in result:
                print(i)
                try:
                    writer.writerow([i[0], i[1].replace("\xa0", " ").replace("\u200b", "")])
                except:
                    """einige wenige Tupel können nicht geschrieben werden"""
                    print("skipline", i)


# sc = SetCrawler()
# sc.crawl_set_prices(["10251", "10270", "10260"])