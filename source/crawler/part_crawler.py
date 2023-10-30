import datetime
from scrapy.crawler import CrawlerProcess
import csv

from unidecode import unidecode

from source.crawler.minifigur_spider import MinifigurSpider
from source.crawler.minifgur_part_spider import MinifigurPartSpider
from source.crawler.design_id_spider import DesignIdSpider
from source.crawler.set_part_spider import SetPartSpider
from source.parser.stueckliste import Stueckliste
from source.Entity.entities import EinzelteilMarktpreis, Einzelteil, Anbieter
from source.utility import preis_zu_float


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
        """crawlt die Einzelteile von Minifiguren zu einem Set"""
        process = CrawlerProcess()
        result = []
        process.crawl(MinifigurPartSpider, url="https://brickset.com/parts/in-" + set_id + "-1/category-" + category + "/page-1",
                      result=result)
        process.start()
        self.save_as_csv(result, "FigureParts " + set_id)

    def crawl_minifigures(self, set_id):
        """Crawlt zu einer Set_id alle Minifiguren"""
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

    def crawl_design_ids(self,bricklink_einzelteile, shop_name, shop_url):
        """Anfrage mit (BricklinkId, BricklinkFarbname, preis)"""
        process = CrawlerProcess()

        """Result enthält (EinzelteilId, LegoFarbname, preis)"""
        values = list(map(lambda a: (a.design_id, a.color_dict), bricklink_einzelteile))
        result = []
        process.crawl(DesignIdSpider,
                      brickset_url="https://brickset.com/parts?",
                      toypro_url="https://www.toypro.com/de/search?",
                      result=result,
                      values=values)
        process.start()


        """markpreise enthällt alle Marktpreise mit der passenden Legoid"""
        marktpreise = []
        for i in result:
            e = EinzelteilMarktpreis(einzelteile=Einzelteil(einzelteil_id=i[0]),
                                 preis=preis_zu_float(i[2]),
                                 url=shop_url,
                                 anbieter=Anbieter(name=shop_name,
                                                   url=shop_url))
            marktpreise.append(e)

        return marktpreise



    """speichert das Result als eine CSV Datei"""
    def save_as_csv(self, result, name):
        """Speichert ein Result als CSV Datei"""

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


