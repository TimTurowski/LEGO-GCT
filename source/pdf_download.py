from source.anleitungs_downloader.pdf_downloader import PdfDownloader


"""Besipiel für das Downloaden einer PDF datei. Wenn die Methode mehrfach ausgweführt werden soll muss die Logik in 
einem Subprozess gekapselt werden"""
p = PdfDownloader()
print(p.download_anleitung(["75191", "75019", "75085"]))