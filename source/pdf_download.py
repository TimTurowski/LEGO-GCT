from source.anleitungs_downloader.pdf_downloader import PdfDownloader
import os


"""Besipiel für das Downloaden einer PDF datei. Wenn die Methode mehrfach ausgweführt werden soll muss die Logik in 
einem Subprozess gekapselt werden"""
p = PdfDownloader()
print(p.download_anleitung(set_ids=["8297"], save_path="./anleitungen/"))

files = os.listdir("./anleitungen/")
for file in files:
    print(file)