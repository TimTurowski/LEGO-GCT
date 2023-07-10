from abc import ABC, abstractmethod


class Crawler(ABC):
    @abstractmethod
    def __init__(self):
        pass

    """in crawlPreis wird eine List von Legoteilen übergeben
    der Rückgabewert ist eine Datenstruktur, welche den jeweiligen Einzelteilen den Preis zuordnet"""
    @abstractmethod
    def crawl_preis(self, legoteile):
        pass
