from multiprocessing import Process
from source.crawler import LegoCrawler
from source.datastructures.einzelteil import Einzelteil


""" funktion wird in einem Prozess ausgeführt"""
def execute_crawling(einzelteile):
    crawler = LegoCrawler()
    result = crawler.crawl_preis(einzelteile)

    for i in result.get_lego_teile():
        print(i.einzelteil.element_id, i.einzelteil.name, i.preis, i.url)

"""ohne main ist Multiprozessing nicht möglich"""
if __name__ == '__main__':
    """erstellt Prozess in welchem der Crawl vorgang gestartet wird dies ermöglicht mehrere Crawl vorgänge"""
    p = Process(target=execute_crawling, args=([Einzelteil("6438899"), Einzelteil("6359941")],))
    p.start()
    p.join()

    p = Process(target=execute_crawling, args=([Einzelteil("6438899"), Einzelteil("6359941")],))
    p.start()
    p.join()
"""Dieser Workaraound ist nicht optimal es gibt probleme wenn den Methoden der Prozesse parameter übergeben werden.
Eine weitere Idee um das Problem das nur ein Crawlvorgang gestartet werden kann ist für jeden Vorgang ein Python 
Script zu straten. Das Problem ist darauf zurück zuführen, dass der reactor für die Internet verbindung während des
Script durchlauf nicht neu gestartet werden kann"""




