from scrapy.crawler import CrawlerProcess

from source.anleitungs_downloader.pdf_spider import PdfSpider

from source.datastructures import DownloadResult

class PdfDownloader():
    def download_anleitung(self,set_ids):
        process = CrawlerProcess()
        result = {}
        process.crawl(PdfSpider, set_ids=set_ids, result=result)
        process.start()

        """textuelle Darstellung als Platzhalter wird später durch entsprechende Entität ersetzt"""
        succesfull_sets = []
        failed_sets = []

        for key in result:
            if result[key] is None:
                failed_sets.append(key)
            elif not result[key][1]:
                failed_sets.append(key)
            else:
                succesfull_sets.append(key + " " + result[key][0])

        download_result = DownloadResult(succesfull_sets, failed_sets)
        return download_result
