import multiprocessing
from multiprocessing import Process

from source.crawler import LegoCrawler
from source.crawler.toypro_crawler import ToyproCrawler
from source.datenbanklogik.datenzugriffsobjekt import Datenzugriffsobjekt
from source.utility.part_logger import PartLogger


def execute_crawling(einzelteile, teile_crawler, mp_queue):
    crawler = teile_crawler
    result = crawler.crawl_preis(einzelteile)
    for i in result.einzelteil_marktpreise:
        mp_queue.put(i)
    mp_queue.put(None)
    for i in result.failed_lego_teile:
        mp_queue.put(i)
    mp_queue.put(None)


    """gibt informationen über den Crawl vorgang aus"""
if __name__ == '__main__':
    dao = Datenzugriffsobjekt()
    mp_queue = multiprocessing.JoinableQueue()

    pl = PartLogger("../setIds/partIds/")
    parts = pl.missing_parts("parts", "parts_toypro_log")
    p = Process(target=execute_crawling, args=(parts, ToyproCrawler(), mp_queue))

    p.start()

    succesfull_marktpreise = []
    failed_marktpreise = []
    while True:
        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            if queue_value.einzelteile.einzelteil_id is not None:
                succesfull_marktpreise.append(queue_value)
    while True:
        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            failed_marktpreise.append(queue_value)

    print(succesfull_marktpreise)
    print(failed_marktpreise)
    dao.fuge_einzelteil_marktpreis_hinzu(succesfull_marktpreise)

    print(f"{len(succesfull_marktpreise)*100/(len(failed_marktpreise) + len(succesfull_marktpreise))}%")
    pl.log_succesful_parts("parts_toypro_log", succesfull_marktpreise)
    pl.log_failed_parts("parts_toypro_log", failed_marktpreise)
    p.join()