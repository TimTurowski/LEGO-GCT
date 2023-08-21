import multiprocessing
import datetime
from multiprocessing import Process

from source.crawler.part_crawler import PartCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
from source.utility.set_logger import SetLogger


def execute_crawling(set_id,set_name, part_crawler, mp_queue):
    crawler = part_crawler
    crawl_result = crawler.crawl_set_parts(set_id, set_name)


    for i in crawl_result.stueckliste:
        mp_queue.put(i)
    mp_queue.put(None)





if __name__ == "__main__":

    sl = SetLogger()
    starttime = datetime.datetime.now()
    year = "2006"
    remaining_sets = sl.missing_set_log(year=year, set_ids_path="../setIds/")
    setcount = 0
    for set in remaining_sets:
        print(set)
        dao = Datenzugriffsobjekt()
        mp_queue = multiprocessing.JoinableQueue()
        """erstellt Prozess in welchem der Crawl vorgang gestartet wird dies ermöglicht mehrere Crawl vorgänge"""
        p = Process(target=execute_crawling, args=(set[0],set[1], PartCrawler(), mp_queue))
        p.start()
        stueckliste = []
        while True:
            queue_value = mp_queue.get()
            if queue_value is None:
                break
            else:
                stueckliste.append(queue_value)

        p.join()
        if len(stueckliste) > 0:
            sl.add_succesful_set(set[0], set[1], year)
            dao.fuge_einzelteil_legoset_hinzu(stueckliste)
        else:
            sl.add_failed_set(set[0], set[1], year)
        setcount = setcount + 1
        print(datetime.datetime.now() - starttime)
        print(f"{setcount}/{len(remaining_sets)}  {setcount * 100 / len(remaining_sets)}%")




