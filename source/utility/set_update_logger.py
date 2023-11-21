import csv
from datetime import datetime
import os
if(os.name == 'posix'):
    from DiscordBot.dc_message import send_discord_message
    from utility.set_logger import SetLogger
else:
    from source.DiscordBot.dc_message import send_discord_message
    from source.utility.set_logger import SetLogger


class SetUpdateLogger:
    def __init__(self, log_path, set_lifetime=5):
        self.log_path = log_path
        self.set_lifetime = set_lifetime
        self.set_logger = SetLogger()
        self.year = str(datetime.now().year)



    """Updated die Log Datei und Sets, welche aktuell Beobachtet werden"""
    def update_sets(self, crawl_result):
        result = []
        set_ids = set(map(lambda n: n[0], crawl_result))
        failed_set_ids = set()


        """einlesen der Sets aus der CSV"""
        with open(self.log_path, newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            """CSV als Liste aufbauen"""
            for row in file_reader:
                """alle Sets in der Watchlist werden um 1 Hochgezählt"""
                if int(row[2]) < self.set_lifetime:
                        result.append([row[0], row[1], int(row[2]) + 1])
                else:
                    """log Eintrag für gescheitertes Set"""
                    self.set_logger.add_failed_set(row[0], row[1], self.year)
                    send_discord_message(f"```ansi\n[0;31m{row[0]}, {row[1]} kann nicht der Datenbank hinzugefügt werden```")
                    failed_set_ids.add(row[0])





            """fügt alle neu Gecrawlten Sets in die Log Datei hinzu"""
            for i in crawl_result:
                if i[0] not in set(map(lambda n: n[0], result)) and i[0] not in failed_set_ids:
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
                else:
                    self.set_logger.add_succesful_set(row[0], row[1], self.year)

            csvfile.close()
        with open(self.log_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for i in result:
                writer.writerow(i)

