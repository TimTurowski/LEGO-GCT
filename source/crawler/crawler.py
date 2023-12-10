from abc import ABC, abstractmethod


class Crawler(ABC):
    """
    Eine Abstrakte Klasse für unsere Shop-Crawler
    """
    @abstractmethod
    def __init__(self):
        pass


    @abstractmethod
    def crawl_preis(self, legoteile):
        """
        Eine abstrakte Methode, welche die Preise zu übergebenen Legoteilen ercrawlen soll
        :param legoteile: eine Liste an Legoteilen
        :type legoteile: Liste mit LegoEinzelteilen
        """
        pass
