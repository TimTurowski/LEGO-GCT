import csv

"""hilfsmethode zum vergleichen von csv Dateien 
compare liefert eine textuelle Darstellung zum vergleich zwischen zwei CSV Dateien, welche Set IDs beinhalten"""
def compare(file1, file2):

    set_a = set()
    with open(file1, newline="" , encoding='utf-8') as csvfile:
        file_reader1 = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in file_reader1:
            set_a.add((row[0],row[1]))
    set_b = set()
    with open(file2, newline="" , encoding='utf-8') as csvfile:
        file_reader2 = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in file_reader2:
            set_b.add((row[0],row[1]))

    result = "in file " + file1.split('/')[-1] + " und in file" + file2.split('/')[-1] + "\n"
    for i in set_a.intersection(set_b):
        result = result + "   "+ i[0] + " " + i[1] + "\n"

    result = result + "nur in file " + file1.split('/')[-1] + "\n"
    for i in set_a.difference(set_a.intersection(set_b)):
        result = result + "   " + i[0] + " " + i[1] + "\n"

    result = result + "nur in file " + file2.split('/')[-1] + "\n"
    for i in set_b.difference(set_a.intersection(set_b)):
        result = result + "   " + i[0] + " " + i[1] + "\n"

    return result



print(compare("../setIds/280723.csv", "../setIds/310723.csv"))

