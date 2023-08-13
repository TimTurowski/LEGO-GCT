import csv

class SetUpdateLogger:
    def __init__(self, log_path, set_lifetime=5):
        self.log_path = log_path
        self.set_lifetime = set_lifetime

    """Updated die Log Datei und Sets, welche aktuell Beobachtet werden"""
    def update_sets(self, crawl_result):
        result = []
        set_ids = set(map(lambda n: n[0], crawl_result))
        """einlesen der Sets aus der CSV"""
        with open(self.log_path, newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            """CSV als Liste aufbauen"""
            for row in file_reader:
                """ist das Set in der Menge der aktuell gecrawlten Sets? Dann wird das Set einfach ohne veränderung in 
                die Liste aufgenommen"""
                if row[0] in set_ids:
                    result.append([row[0], row[1], row[2]])
                else:
                    """Set wird nicht gecrawlt. Dann wird der Counter des Sets um 1 erhöht. Wird ein Schwellenwert 
                    überschritten beim Counter wird das Set nicht weiter berücksichtigt so werden Sets ohne Anleitung 
                    gefiltert"""
                    if int(row[2]) < self.set_lifetime:
                        result.append([row[0], row[1], int(row[2]) + 1])

            """fügt alle neu Gecrawlten Sets in die Log Datei hinzu"""
            for i in crawl_result:
                if i[0] not in set(map(lambda n: n[0], result)):
                    result.append([i[0], i[1], 0])
            csvfile.close()

        with open(self.log_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for i in result:

                writer.writerow(i)
    """gibt alle Sets die aktuell Beobachtet werden  aus"""
    def get_sets(self):

        result = []
        with open(self.log_path, newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                result.append([row[0], row[1]])
        return result
    """entfernt erfolgreich aufgenommene Sets aus der Beobachtungsliste"""
    def remove_succesful_sets(self,succesful_sets):
        result = []
        with open(self.log_path, newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                if row[0] not in succesful_sets:
                    result.append(row)
            csvfile.close()
        with open(self.log_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for i in result:
                writer.writerow(i)

