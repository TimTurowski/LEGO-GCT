from scrapy.crawler import CrawlerProcess
import csv
import os
if(os.name == 'posix'):
    from crawler.minifigur_spider import MinifigurSpider
    from crawler.minifgur_part_spider import MinifigurPartSpider
    from crawler.design_id_spider import DesignIdSpider
    from crawler.part_details_spider import PartDetailsSpider
    from crawler.set_part_spider import SetPartSpider
    from parser.stueckliste import Stueckliste
    from Entity.entities import EinzelteilMarktpreis, Einzelteil, Anbieter, Einzelteildetails, Kategorie
    from utility import preis_zu_float
else:
    from source.crawler.minifigur_spider import MinifigurSpider
    from source.crawler.minifgur_part_spider import MinifigurPartSpider
    from source.crawler.design_id_spider import DesignIdSpider
    from source.crawler.part_details_spider import PartDetailsSpider
    from source.crawler.set_part_spider import SetPartSpider
    from source.parser.stueckliste import Stueckliste
    from source.Entity.entities import EinzelteilMarktpreis, Einzelteil, Anbieter, Einzelteildetails, Kategorie
    from source.utility import preis_zu_float


class PartCrawler:
    """
    Objekte dieser Klasse besitzen Methoden um viele unterschiedliche Informationen zu crawlen
    """


    def crawl_set_parts(self, set_id, set_name):
        """
        Diese Methode crawlt zu einer Set Id die entsprechenden Einzelteile
        :param set_id: Set_ID, zu der die Einzelteile gecrawelt werden sollen
        :type set_id: string
        :param set_name: Name des Sets, dessen Einzelteile gecrawelt werden sollen
        :type set_name: string
        """

        stueckliste = Stueckliste()
        # result enhällt die rohen Informationen über die Einzelteile als Tupel
        results = []
        process = CrawlerProcess()
        process.crawl(SetPartSpider, url="https://brickset.com/parts/in-" + set_id +"-1", result=results)
        process.start()
        for i in results:
            stueckliste.add_to_stueckliste(anzahl=i[1],einzelteil_id=i[0], set_id=set_id, name=set_name)

        return stueckliste

    def crawl_part_details(self, ids):
        """Crawlt die Details der Einzelteile für die übergebenen Set-IDs.

        Diese Methode verwendet einen Spider, um die Beschreibung, Kategorie
        und Farbe der Einzelteile von LEGO-Sets abzurufen.

        :param ids: Eine Liste von Set-IDs, für die die Einzelteildetails abgerufen werden sollen.
        :type ids: list of str
        :return: Eine Liste von Einzelteildetails-Objekten mit den abgerufenen Informationen.
        :rtype: list of Einzelteildetails
        """


        process = CrawlerProcess()

        # speichert die Informationen zwischen
        result = set()
        process.crawl(PartDetailsSpider,
                      url="https://brickset.com/parts/in-",
                      ids=ids,
                      result=result)
        process.start()

        detail_liste = []
        # erstellt die Objekte für die DB
        for i in result:
            detail_liste.append(Einzelteildetails(einzelteile=Einzelteil(einzelteil_id=i[0]),
                                                   beschreibung=i[1],
                                                   kategorie=Kategorie(kategorie_id=i[2]),
                                                   farbe=i[3]))

        return detail_liste


    def crawl_design_ids(self,bricklink_einzelteile, shop_name, shop_url):
        """Crawlt aus übergeben Bricklink design Ids mit dem Passenden Farbcode
        die richtige Element Id und erstelt ein Marktpreis Objekt"""
        process = CrawlerProcess()

        # baut eine Datenstruktur für den Crawler auf
        # color_dict ist ein Dictionary, welches den Farbcode zum Preis zuordnet
        values = list(map(lambda a: (a.design_id, a.color_dict), bricklink_einzelteile))
        result = []
        process.crawl(DesignIdSpider,
                      brickset_url="https://brickset.com/parts?",
                      toypro_url="https://www.toypro.com/de/search?",
                      result=result,
                      values=values)
        process.start()

        # markpreise enthält alle Marktpreise mit dem passenden Element id
        marktpreise = []
        for i in result:
            e = EinzelteilMarktpreis(einzelteile=Einzelteil(einzelteil_id=i[0]),
                                 preis=preis_zu_float(i[2]),
                                 url=shop_url,
                                 anbieter=Anbieter(name=shop_name,
                                                   url=shop_url))
            marktpreise.append(e)

        return marktpreise

    def crawl_figure_parts_to_set(self, set_id, category):
        """crawlt die Einzelteile von Minifiguren zu einem Set"""
        process = CrawlerProcess()
        result = []
        process.crawl(MinifigurPartSpider,
                      url="https://brickset.com/parts/in-" + set_id + "-1/category-" + category + "/page-1",
                      result=result)
        process.start()
        self.save_as_csv(result, "FigureParts " + set_id)

    def crawl_minifigures(self, set_id):
        """Crawlt zu einer Set_id alle Minifiguren"""
        process = CrawlerProcess()
        result = []
        process.crawl(MinifigurSpider, url="https://brickset.com/minifigs/in-" + set_id + "-1",
                      result=result)
        process.start()
        self.save_as_csv(result, "Minifigures " + set_id)



    def save_as_csv(self, result, name):
        """Speichert ein Result als CSV Datei"""

        with open("../setIds/minifigures/" + name + ".csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in result:
                try:
                    if len(i) == 2:
                        writer.writerow([i[0], i[1].replace("\xa0", " ").replace("\u200b", "")])
                    elif len(i) == 3:
                        writer.writerow([i[0], i[1].replace("\xa0", " ").replace("\u200b", ""), i[2]])
                except:
                    # einige wenige Tupel können nicht geschrieben werden
                    pass

