import datetime
from scrapy.crawler import CrawlerProcess
import csv

from unidecode import unidecode

from source.crawler.minifigur_spider import MinifigurSpider
from source.crawler.minifgur_part_spider import MinifigurPartSpider
from source.crawler.set_part_spider import SetPartSpider
from source.parser.stueckliste import Stueckliste

class PartCrawler:


    def crawl_head_parts(self):
        process = CrawlerProcess()
        result = []
        process.crawl(MinifigurPartSpider, url="https://brickset.com/parts/category-Figure-Wigs/page-1", result=result)
        process.start()
        self.save_as_csv(result, "HeadParts")

    def crawl_figure_parts(self):
        process = CrawlerProcess()
        result = []
        process.crawl(MinifigurPartSpider, url="https://brickset.com/parts/category-Figure-Parts/page-1", result=result)
        process.start()
        self.save_as_csv(result, "FigureParts")

    def crawl_figure_parts_to_set(self, set_id, category):
        process = CrawlerProcess()
        result = []
        process.crawl(MinifigurPartSpider, url="https://brickset.com/parts/in-" + set_id + "-1/category-" + category + "/page-1",
                      result=result)
        process.start()
        self.save_as_csv(result, "FigureParts " + set_id)

    def crawl_minifigures(self, set_id):
        process = CrawlerProcess()
        result = []
        process.crawl(MinifigurSpider, url="https://brickset.com/minifigs/in-"+set_id+"-1",
                      result=result)
        process.start()
        self.save_as_csv(result, "Minifigures " + set_id)
    def crawl_set_parts(self, set_id, set_name):
        liste = Stueckliste()
        results = []
        process = CrawlerProcess()
        process.crawl(SetPartSpider, url="https://brickset.com/parts/in-" + set_id +"-1", result=results)
        process.start()
        for i in results:
            liste.add_to_stueckliste(anzahl=i[1],einzelteil_id=i[0], set_id=set_id, name=set_name)

        return liste

    """speichert das Result als eine CSV Datei"""
    def save_as_csv(self, result, name):

        with open("../setIds/minifigures/" + name + ".csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in result:
                print(i)
                try:
                    if len(i) == 2:
                        writer.writerow([i[0], i[1].replace("\xa0", " ").replace("\u200b", "")])
                    elif len(i) == 3:
                        writer.writerow([i[0], i[1].replace("\xa0", " ").replace("\u200b", ""), i[2]])
                except:
                    """einige wenige Tupel können nicht geschrieben werden"""
                    print("skipline", i)

pc = PartCrawler()
print(pc.crawl_minifigures("75313"))