from scrapy.crawler import CrawlerProcess
import csv

from source.crawler.set_spider import SetSpider


class SetCrawler:

    def crawl_set_ids(self, year):
        process = CrawlerProcess()
        result = []
        process.crawl(SetSpider, url="https://www.steinelager.de/de/sets/year/" + year +"/1", result=result)
        process.start()



        with open("../setIds/"+year+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            for i in result:
                try:
                    writer.writerow([i[0], i[1]])
                except:
                    print("skipline", i)
sc = SetCrawler()
sc.crawl_set_ids("2022")