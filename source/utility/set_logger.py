import csv
import os
import datetime

if(os.name == 'posix'):
    LOGS_PATH = "/home/student/LEGO-GCT/source/setIds/logs/"
    SET_IDS = "/home/student/LEGO-GCT/source/setIds/"
else:
    LOGS_PATH = "../setIds/logs/"
    SET_IDS = "../setIds/"

class SetLogger:

    def __init__(self):
        year = datetime.datetime.now().year
        file_name = SET_IDS + f"{year}.csv"
        if not os.path.exists(file_name):
            open (file_name, 'w')

        file_name = LOGS_PATH + f"{year}_log.csv"
        if not os.path.exists(file_name):
            open(file_name, 'w')


    def add_succesful_set(self, id, name, year, log_path=LOGS_PATH):

        with open(log_path + year + "_log.csv", 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([id, name.replace("\xa0", " ").replace("\u200b", ""), True])

    def add_failed_set(self, id, name, year, log_path=LOGS_PATH):
        with open(log_path + year + "_log.csv", 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([id, name.replace("\xa0", " ").replace("\u200b", ""), False])

    def succesful_set_log(self, year, log_path=LOGS_PATH):
        result = []
        with open(log_path + year + "_log.csv", newline="", encoding='utf-8') as csvfile:


            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                if row[2] == "True":
                    result.append(row)
        return result

    def failed_set_log(self, year, log_path=LOGS_PATH):
        result = []
        with open(log_path + year + "_log.csv", newline="", encoding='utf-8') as csvfile:


            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                if row[2] == "False":
                    result.append(row)
        return result
    def missing_set_log(self, year, set_ids_path=SET_IDS):
        available_sets = set()
        with open(set_ids_path+"/logs/" + year + "_log.csv", newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                available_sets.add(row[0])

        result = []
        with open(set_ids_path + year + ".csv", newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                if row[0] not in available_sets:
                    result.append(row)
        return result




