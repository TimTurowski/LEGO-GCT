import os
from pikepdf import Pdf
from scrapy.crawler import CrawlerProcess

if(os.name == 'posix'):
    from anleitungs_downloader.pdf_spider import PdfSpider
    from datastructures import DownloadResult
else:
    from source.anleitungs_downloader.pdf_spider import PdfSpider
    from source.datastructures import DownloadResult

class PdfDownloader():
    """
    Objekte dieser Klasse besitzen Methoden zum Downloaden und Verkürzen von Anleitungs PDF
    """
    def download_anleitung(self,set_ids, save_path="./anleitungen/"):
        """
        Diese Funktion enthält die Logik des Anleitung Downloadens
        :param set_ids: Die ID des Legosets, dessen Anleitung runtergladen werden soll
        :type set_ids: string
        :param save_path: Angabe des Pfades, wo die PDF gespeichert werden sollen, standardmäßig angegeben
        :type save_path: string
        """
        process = CrawlerProcess()
        result = {}
        process.crawl(PdfSpider, set_ids=set_ids, result=result, path_base=save_path)
        process.start()

        succesfull_sets = []
        failed_sets = []

        # aufteilen der URLs in Listen zur späteren verarbeitung
        for key in result:
            if not result[key]:
                failed_sets.append(key)
            elif not result[key] or result[key] is None:
                failed_sets.append(key)
            else:
                succesfull_sets.append(key + " " + str(result[key]))

        # Speichern der Listen in ein download_result objekt
        download_result = DownloadResult(succesfull_sets, failed_sets)
        return download_result

    def cut_anleitungen(self, source_path, destination_path, cut_pages=10):
        """
        Diese Funktion verkürzt alle Anleitungs PDF
        :param source_path: Pfadangabe der ungekürzten PDF
        :type source_path: string
        :param destination_path: Pfadangabe wohin gekürzte PDF gespeichert werden sollen
        :type destination_path: string
        :param cut_pages: Anzahl, wieviele letzte Pages abgespeichert werden sollen
        :type cut_pages: int
        """

        files = os.listdir(source_path)
        for file in files:
            pdf = Pdf.open(source_path + file)
            file2pages = {
                0: [0, max(0, len(pdf.pages) - cut_pages)],
                1: [max(0, len(pdf.pages) - cut_pages), len(pdf.pages)],
            }
            new_pdf_files = [Pdf.new() for i in file2pages]
            # Index für die Numerierung der PDF Teile
            new_pdf_index = 0

            for n, page in enumerate(pdf.pages):
                if n in list(range(*file2pages[new_pdf_index])):
                    new_pdf_files[new_pdf_index].pages.append(page)

                else:
                    # nächste Datei
                    new_pdf_index += 1
                    new_pdf_files[new_pdf_index].pages.append(page)

            # save the last PDF file
            name, ext = os.path.splitext(destination_path+file)
            output_filename = f"{name}-cut.pdf"
            new_pdf_files[new_pdf_index].save(output_filename)
            print(f"[+] File: {output_filename} saved.")



