
class DownloadResult:

    def __init__(self, succesful_sets, failed_sets):
        self.__succesful_sets = succesful_sets
        self.__failed_sets = failed_sets

    @property
    def succesful_sets(self):
        return self.__succesful_sets
    @succesful_sets.setter
    def succesful_sets(self, new_succesful_sets):
        self.__succesful_sets = new_succesful_sets

    @property
    def failed_sets(self):
        return self.__failed_sets
    @failed_sets.setter
    def failed_sets(self, new_failed_sets):
        self.__failed_sets = new_failed_sets

    """__str__ muss angepasst werden wenn Entitys implementiert sind"""
    def __str__(self):
        s = ""
        if len(self.succesful_sets) > 0:
            s = "Erfolgreich Heruntergeladene Anleitungen:\n"

        for i in self.succesful_sets:
            s = s + "   " + i + "\n"

        if len(self.failed_sets) > 0:
            s = s + "Gescheiterte Sets:\n"
        for i in self.failed_sets:
            s = s + "   " + i + "\n"
        return  s

