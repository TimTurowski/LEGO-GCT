import csv

from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt

def get_added_sets():
    existing_set_prices = set()
    with open("sets.csv", newline="", encoding='utf-8') as csvfile:

        file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in file_reader:
            existing_set_prices.add(row[0])

    return existing_set_prices



if __name__ == "__main__":
    dao = Datenzugriffsobjekt()
    ids = set(map(lambda a:a.set_id, dao.lego_set_liste()))
    added_sets = get_added_sets()
    with open("sets.csv", 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in ids:
            writer.writerow([i, True])

    print(ids - added_sets)

