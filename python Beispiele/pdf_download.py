import datetime

from source.anleitungs_downloader.pdf_downloader import PdfDownloader
import os


"""Besipiel für das Downloaden einer PDF datei. Wenn die Methode mehrfach ausgweführt werden soll muss die Logik in 
einem Subprozess gekapselt werden"""
start_time = datetime.datetime.now()
p = PdfDownloader()
print(p.download_anleitung(set_ids=["75060"], save_path="./anleitungen/"))
p.cut_anleitungen(source_path="./anleitungen/", destination_path="./anleitungen/")
files = os.listdir("./anleitungen/")
print((datetime.datetime.now() - start_time).total_seconds())
for file in files:
    print(file)