import csv

from source.Entity.entities import Einzelteil


class PartLogger:
    def __init__(self, path):
        self.path = path

    def write_ids(self, name, ids):
        with open(self.path + name + ".csv", 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in ids:
                writer.writerow([i.einzelteil_id])

    def log_succesful_parts(self, name, ids):
        with open(self.path + name + ".csv", 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in ids:
                writer.writerow([i.einzelteile.einzelteil_id, True])
    def log_failed_parts(self, name, ids):
        with open(self.path + name + ".csv", 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in ids:
                writer.writerow([i.einzelteil_id, False])
    def missing_parts(self, name, log_name):
        available_parts = set()
        with open(self.path + log_name +".csv", newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                available_parts.add(row[0])

        result = []
        with open(self.path + name + ".csv", newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                if row[0] not in available_parts:
                    result.append(Einzelteil(einzelteil_id=row[0]))
        return result