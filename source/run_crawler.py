from multiprocessing import Process
from source.crawler import LegoCrawler
from source.datastructures.einzelteil import Einzelteil

"""Diese Datei ist eine Art beispiel Geschäftslogik in welcher der Crawler ausgeführt werden kann"""

""" funktion wird in einem Prozess ausgeführt als Parameter muss eine Liste von
Einzelteilen übergeben werden auch bei nur einem Einzelteil"""


def execute_crawling(einzelteile):
    crawler = LegoCrawler()
    result = crawler.crawl_preis(einzelteile)
    """gibt informationen über den Crawl vorgang aus"""
    print(result)


"""ohne main ist Multiprocessing nicht möglich"""

if __name__ == '__main__':
    """erstellt Prozess in welchem der Crawl vorgang gestartet wird dies ermöglicht mehrere Crawl vorgänge"""
    p = Process(target=execute_crawling, args=([Einzelteil("6438898"), Einzelteil("6438899")],))
    p.start()
    p.join()

    p = Process(target=execute_crawling, args=([Einzelteil("6435857"),
                                                Einzelteil("6406522"),
                                                Einzelteil("6411329"),
                                                Einzelteil("6390506"),
                                                Einzelteil("6360199")],))
    p.start()
    p.join()
"""Eine weitere Idee um das Problem das nur ein Crawl vorgang gestartet werden kann ist für jeden Vorgang ein Python 
Script zu starten. Das Problem ist darauf zurück zuführen, dass der reactor für die Internet verbindung während des
Script durchlauf nicht neu gestartet werden kann"""
