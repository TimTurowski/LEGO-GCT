import datetime


class CrawlResult:
    """Objekte der Klasse CrawlResult sammeln alle informationen, welche bei einem Crawl Vorgang
    zusammengetragen wurden"""
    def __init__(self, einzelteil_marktpreise, failed_lego_teile, crawl_duration):
        self.__einzelteil_marktpreise = einzelteil_marktpreise
        self.__failed_lego_teile = failed_lego_teile
        self.__crawl_duration = crawl_duration
        self.__crawl_datetime = datetime.datetime.now()


    @property
    def einzelteil_marktpreise(self):
        """Diese Funktion gibt eine Liste von EinzelteilMarktpreisen zurück"""

        return self.__einzelteil_marktpreise

    @einzelteil_marktpreise.setter
    def einzelteil_marktpreise(self, new_einzelteil_marktpreise):
        """Diese Funktion speichert eine Liste von EinzelteilMarktpreisen
        :param new_einzelteil_marktpreise: eine Liste mit EinzelteilMarktpreisen
        :type new_einzelteil_marktpreise: Liste von EinzelteilMarktpreisen
        """

        self.__einzelteil_marktpreise = new_einzelteil_marktpreise


    @property
    def failed_lego_teile(self):
        """
        Diese Funktion gibt eine Liste mit Legoeinzelteilen zurück, dessen CrawlVorgänge schiefgelaufen sind
        """
        return self.__failed_lego_teile

    @failed_lego_teile.setter
    def failed_lego_teile(self, new_failed_lego_teile):
        """
        Diese Funktion speichert ein Liste an Legoeinzelteilen als beim Crawl Vorgang fehgeschlagen
        :param new_failed_lego_teile: eine Liste von Legoeinzelteilen, dessen Crawl Vorgang nicht erfolgreich war
        :type new_failed_lego_teile: Liste von LegoEinzelteilen
        """
        self.__failed_lego_teile = new_failed_lego_teile


    @property
    def success_rate(self):
        """Diese Funktion gibt die Erfolgsrate des Crawl Vorgangs Zurück
        """

        return len(self.__einzelteil_marktpreise) / (len(self.__einzelteil_marktpreise) + len(self.__failed_lego_teile))


    @property
    def crawl_duration(self):
        """Diese Funktion gibt die Crawl Dauer zurück"""
        return self.__crawl_duration


    @property
    def crawl_datetime(self):
        """Diese Funktion gibt den Zeitpunkt des Crawlvorgangs zurück"""
        return self.__crawl_datetime

    def __str__(self):
        if len(self.__einzelteil_marktpreise) > 0:
            s = "erfolgreich gecrawlte Einzelteile:\n"
        else:
            s = ""

        for i in self.__einzelteil_marktpreise:
            s = s + "   " + str(i) + "\n"

        if len(self.failed_lego_teile) > 0:
            s = s + "gescheiterte Einzelteile:\n"
        else:
            s = s + ""

        for i in self.__failed_lego_teile:
            s = s + "   " + str(i) + "\n"
        s = s + "Die Erfolgsrate des Crawlvorgangs liegt bei " + "{:.0%}".format(self.success_rate)
        return s
