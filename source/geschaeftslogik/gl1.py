import multiprocessing
from multiprocessing import Process
from source.crawler import LegoCrawler
from source.crawler.toypro_crawler import ToyproCrawler
from source.Entity.entities import Einzelteil
from source.utility.visualisation import show_marktpreis_comparision
from source.anleitungs_downloader.pdf_downloader import PdfDownloader

def execute_download():
    p = PdfDownloader()
    print(p.download_anleitung(set_ids=["8297"], save_path="./temp_downloader/"))

if __name__ == "__main__":
    p = Process(target=execute_download)
    p.start()
    p.join()


