import csv

class SetUpdateLogger:


    def update_sets(self, log_path, crawl_result):
        result = []
        set_ids = set(map(lambda n: n[0], crawl_result))

        with open(log_path, newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                if row[0] in set_ids:
                    result.append([row[0], row[1], row[2]])
                else:
                    if int(row[2]) < 10:
                        result.append([row[0], row[1], int(row[2]) + 1])

            for i in crawl_result:
                if i[0] not in set(map(lambda n: n[0], result)):
                    result.append([i[0], i[1], 0])
            csvfile.close()

        with open(log_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for i in result:

                writer.writerow(i)
    def remove_succesful_sets(self, log_path,succesful_sets):
        result = []
        with open(log_path, newline="", encoding='utf-8') as csvfile:

            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in file_reader:
                if row[0] not in succesful_sets:
                    result.append(row)
            csvfile.close()
        with open(log_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for i in result:
                writer.writerow(i)




a = SetUpdateLogger()
result = [('76994', 'Sonic'),('40628', 'Miles „Tails“ Prower'),
          ("42157","John (Deere 948L-II Skidder"),
          ("42160","Audi RS Q e-tron"),
          ("42161","Lamborghini Huracán Tecnica")]
a.update_sets(log_path="tracked_sets_test.csv", crawl_result=result)
succesfull = set(['76994'])
a.remove_succesful_sets("tracked_sets_test.csv",succesfull)