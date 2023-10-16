import datetime
from scrapy.crawler import CrawlerProcess
import csv

from unidecode import unidecode

from source.crawler.set_spider import SetSpider

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
        process.crawl(SetSpider, url="https://www.steinelager.de/de/sets/p/1?availability=1", result=result)
        process.start()

        """CSV Datei wird im Fromat DDMMYY gespeichert"""
        date = datetime.datetime.now()
        # self.save_as_csv(result, date.strftime("%d") + date.strftime("%m") + date.strftime("%y"))
        return result

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

