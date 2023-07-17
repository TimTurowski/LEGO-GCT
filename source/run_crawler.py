import multiprocessing
from multiprocessing import Process
from source.crawler import LegoCrawler
from source.crawler.toypro_crawler import ToyproCrawler
from source.datastructures.einzelteil import Einzelteil
from source.utility.visualisation import show_marktpreis_comparision

"""Diese Datei ist eine Art beispiel Geschäftslogik in welcher der Crawler ausgeführt werden kann"""

""" funktion wird in einem Prozess ausgeführt als Parameter muss eine Liste von
Einzelteilen übergeben werden auch bei nur einem Einzelteil"""


def execute_crawling(einzelteile, teile_crawler, conn2):
    crawler = teile_crawler
    result = crawler.crawl_preis(einzelteile)
    """gibt informationen über den Crawl vorgang aus"""
    conn2.send(result)
    # print(result)


"""ohne main ist Multiprocessing nicht möglich"""

if __name__ == '__main__':
    sample_einzelteile = [Einzelteil("6435857"),
                          Einzelteil("6406522"),
                          Einzelteil("6411329"),
                          Einzelteil("6390506"),
                          Einzelteil("6360199")]

    """multiprocessing Pipe ermöglicht den Zugriff auf Objekte aus einem anderen Prozess
     conn1 für recieve und conn2 für send"""

    conn1, conn2 = multiprocessing.Pipe()
    """erstellt Prozess in welchem der Crawl vorgang gestartet wird dies ermöglicht mehrere Crawl vorgänge"""
    p = Process(target=execute_crawling, args=(sample_einzelteile,LegoCrawler(),conn2))
    p.start()
    p.join()
    lego_crawl_result = conn1.recv()
    """Startet den Prozess für Toypro"""
    p = Process(target=execute_crawling, args=(sample_einzelteile,ToyproCrawler(),conn2,))
    p.start()
    p.join()
    toypro_crawl_result = conn1.recv()
    """stellt die marktpreise der Crawl vorgänge tabellarisch dar"""
    show_marktpreis_comparision(lego_crawl_result.einzelteil_marktpreise, toypro_crawl_result.einzelteil_marktpreise)

"""Eine weitere Idee um das Problem das nur ein Crawl vorgang gestartet werden kann ist für jeden Vorgang ein Python 
Script zu starten. Das Problem ist darauf zurück zuführen, dass der reactor für die Internet verbindung während des
Script durchlauf nicht neu gestartet werden kann"""
