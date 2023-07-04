from datetime import datetime

"""Objekte der Klasse CrawlResult repräsentieren alle informationen, welche bei einem Crawlvorgang 
zusammen getragen worden"""


class CrawlResult:
    def __init__(self, preis_lego_teile, failed_lego_teile, success_rate, crawl_duration):
        self.__preis_lego_teile = preis_lego_teile
        self.__failed_lego_teile = failed_lego_teile
        self.__success_rate = success_rate
        self.__crawl_duration = crawl_duration
        self.__crawl_datetime = datetime.datetime.now()

    """gibt Objekt zurück, welches zu den Legoteilen den gecrawlten Preis verwaltet"""

    def get_lego_teile(self):
        return self.__preis_lego_teile

    """gibt die Gescheiterten Legoteile in einer Liste Zurück"""

    def get_failed_lego_teile(self):
        return self.__failed_lego_teile

    """gibt die Erfolgrate des Crawling vorgangs Zurück"""

    def get_succes_rate(self):
        return self.__success_rate

    """gibt die Crawl Dauer zurück"""

    def get_crawl_duration(self):
        return self.__crawl_duration

    """gibt den Zeitpunkt des Crawlvorgangs zurück"""

    def get_crawl_datetime(self):
        return self.__crawl_datetime
