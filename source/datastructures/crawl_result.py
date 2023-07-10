
"""Objekte der Klasse CrawlResult repräsentieren alle informationen, welche bei einem crawl Vorgang 
zusammen getragen worden"""
import datetime


class CrawlResult:
    def __init__(self, einzelteil_marktpreise, failed_lego_teile, success_rate, crawl_duration):
        self.__einzelteil_marktpreise = einzelteil_marktpreise
        self.__failed_lego_teile = failed_lego_teile
        self.__crawl_duration = crawl_duration
        self.__crawl_datetime = datetime.datetime.now()

    """gibt Objekt zurück, welches zu den Legoteilen den gecrawlten Preis verwaltet"""
    @property
    def einzelteil_marktpreise(self):

        return self.__einzelteil_marktpreise

    @einzelteil_marktpreise.setter
    def einzelteil_marktpreise(self, new_einzelteil_marktpreise):

        self.__einzelteil_marktpreise = new_einzelteil_marktpreise

    """gibt die Gescheiterten Legoteile in einer Liste Zurück"""
    @property
    def failed_lego_teile(self):
        return self.__failed_lego_teile

    @failed_lego_teile.setter
    def failed_lego_teile(self, new_failed_lego_teile):
        self.__failed_lego_teile = new_failed_lego_teile

    """gibt die Erfolgsrate des Crawling vorgangs Zurück"""
    @property
    def success_rate(self):
        return len(self.__einzelteil_marktpreise)/(len(self.__einzelteil_marktpreise) + len(self.__failed_lego_teile))

    """gibt die Crawl Dauer zurück"""
    @property
    def crawl_duration(self):
        return self.__crawl_duration

    """gibt den Zeitpunkt des Crawlvorgangs zurück"""

    @property
    def crawl_datetime(self):
        return self.__crawl_datetime

    def __str__(self):
        if len(self.__einzelteil_marktpreise) > 0:
            s = "erfolgreich gecrawlte Einzelteile:\n"
        else:
            s= ""

        for i in self.__einzelteil_marktpreise:
            s = s + "   " + str(i) + "\n"

        if len(self.failed_lego_teile) > 0:
            s = s + "gescheiterte Einzelteile:\n"
        else:
            s = s + ""

        for i in self.__failed_lego_teile:
            s = s + "   " + str(i) + "\n"
        s = s + "Die Erfolgsrate des Crawlvorgangs liegt bei " + "{:.0%}".format(self.success_rate)
        return  s


