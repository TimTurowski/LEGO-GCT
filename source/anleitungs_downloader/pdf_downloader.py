from scrapy.crawler import CrawlerProcess

from source.anleitungs_downloader.pdf_spider import PdfSpider

from source.datastructures import DownloadResult

class PdfDownloader():
    def download_anleitung(self,set_ids, save_path="./anleitungen/"):
        process = CrawlerProcess()
        result = {}
        process.crawl(PdfSpider, set_ids=set_ids, result=result, path_base=save_path)
        process.start()

        """textuelle Darstellung als Platzhalter wird später durch entsprechende Entität ersetzt"""
        succesfull_sets = []
        failed_sets = []

        for key in result:
            if not result[key]:
                failed_sets.append(key)
            elif not result[key] or result[key] is None:
                failed_sets.append(key)
            else:
                succesfull_sets.append(key + " " + str(result[key]))

        download_result = DownloadResult(succesfull_sets, failed_sets)
        return download_result
