import datetime
from scrapy.crawler import CrawlerProcess
import csv
import os

from unidecode import unidecode
if(os.name == 'posix'):
    from crawler.image_spider import SetImageSpider
    from crawler.set_price_spider import SetPriceSpider
    from crawler.set_spider import SetSpider
    from utility.set_logger import SetLogger
else:
    from source.crawler.image_spider import SetImageSpider
    from source.crawler.set_price_spider import SetPriceSpider
    from source.crawler.set_spider import SetSpider
    from source.utility.set_logger import SetLogger


class SetCrawler:
    """
    Ein SetCrawler crawlt Sets. Die verschiedenen Methoden dienen verschiedenen Suchparametern
    """
    def crawl_set_ids(self, year):
        """
        Diese Funktion sucht zu einem angegebenen Jahr alle Sets. Gecrawlte Informationen sind SetID und SetNamen.
        :param year: Jahr, aus denen alle veröffentlichten Sets gesucht werden sollen
        :type year: string
        """
        process = CrawlerProcess()
        result = []
        process.crawl(SetSpider, url="https://www.steinelager.de/de/sets/year/" + year +"/1", result=result)
        process.start()
        self.save_as_csv(result, year)


    def crawl_unreleased_sets(self):
        """
        Diese Funktion crawlt alle Sets, welche noch nicht veröffentlicht worden sind
        """
        process = CrawlerProcess()
        result = []
        year = str(datetime.datetime.now().year)
        process.crawl(SetSpider, url="https://www.steinelager.de/de/sets/year/" + year + "/1", result=result)
        process.start()

        sl = SetLogger()

        # oldset hat alle Sets die bereits in der DB sind oder keine Anleitung haben aus dem aktuellen jahr

        old_sets = sl.succesful_set_log(year) + sl.failed_set_log(year)
        old_sets = list(map(lambda a: (a[0], a[1]), old_sets))


        result = list(map(lambda a: (a[0], a[1].replace("\xa0", " ").replace("\u200b", "")), result))

        new_sets = list(set(result) - set(old_sets))



        ## CSV Datei wird im Fromat DDMMYY gespeichert
        # date = datetime.datetime.now()
        # self.save_as_csv(result, date.strftime("%d") + date.strftime("%m") + date.strftime("%y"))
        return new_sets

    def crawl_set_prices(self, set_ids):
        """
        Diese Funktion crawlt zu übergebenen Set-IDs die SetPreise
        :param set_ids: Eine Liste von Set-IDs dessen Preise gecrawlt werden sollen
        :type set_ids: Liste von Set_id
        """
        process = CrawlerProcess()
        results = [];
        process.crawl(SetPriceSpider, set_ids=set_ids, result=results)
        process.start()
        return results

    def crawl_set_image(self, set_ids):
        """
        Diese Funktion crawlt zu übergebenen Set-IDs die SetBilder
        :param set_ids: Eine Liste von Set-IDs dessen Bilder gecrawlt werden sollen
        :type set_ids: Liste von Set_id
        """
        process = CrawlerProcess()
        results = [];
        process.crawl(SetImageSpider, set_ids=set_ids, result=results)
        process.start()
        return results


    def save_as_csv(self, result, name):
        """
        Diese Funktion speichert eine Liste von Set_IDs in eine CSV Datei
        :param result: Liste von Set_IDs, welche gespeichert werden sollen
        :type result: Liste von Set_id
        :param name: Name, den die CSV Datei haben soll
        :type name: string
        """
        with open("../setIds/" + name + ".csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in result:
                print(i)
                try:
                    writer.writerow([i[0], i[1].replace("\xa0", " ").replace("\u200b", "")])
                except:
                    # einige wenige Tupel können nicht geschrieben werden
                    print("skipline", i)