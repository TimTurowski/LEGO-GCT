from abc import ABC, abstractmethod


class Crawler(ABC):
    @abstractmethod
    def __init__(self):
        pass

    """in crawlPreis wird eine List von Legoteilen übergeben
    der Rückgabewert ist eine Datenstrucktur, welche den jeweiligen Einzelteilen den Preis zuordnet"""
    @abstractmethod
    def crawl_preis(self, legoteile):
        pass

    """getCrawlDuration gibt die Dauer des letzten Crawlvorgangs zurück"""
    def __get_crawl_duration(self):
        return self.crawlDuration

    """getSuccesrate gibt die Erfolgrate des letzten Crawlvorgangs zurück wie groß ist der Anteil der Teile,
    zu welchen ein Preis gefunden wurde"""
    def __get_succesrate(self):
        return self.succesrate
