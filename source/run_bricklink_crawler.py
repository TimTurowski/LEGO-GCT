import multiprocessing
from multiprocessing import Process

from source.crawler.part_crawler import PartCrawler
from source.datastructures.bricklink_einzelteil import BricklinkEinzelteil
from source.geschaeftslogik.bricklink_crawler import BricklinkCrawler


def execute_bricklink_crawling(mp_queue, shop_url, shop_name):
    print(mp_queue)
    bricklink_crawler = BricklinkCrawler()
    result = bricklink_crawler.crawl(
        shop_url,
        shop_name,
        3)
    """Legt alle Objekte in der Queue ab"""
    for i in result:
        mp_queue.put(i)
    mp_queue.put(None)

def execute_id_translation(crawl_result, shop_url, shop_name):
    part_crawler = PartCrawler()
    result = part_crawler.crawl_design_ids(crawl_result, shop_url, shop_name)
    print(result)

if __name__ == '__main__':

    shop_url ="https://store.bricklink.com/generationbrick?p=generationbrick#/shop?o={%22itemType%22:%22P%22,%22catID%22:%223%22,%22showHomeItems%22:0}"
    shop_name ="abc"


    mp_queue = multiprocessing.JoinableQueue()
    p = Process(target=execute_bricklink_crawling, args=[mp_queue, shop_url, shop_name])
    p.start()

    """While Schleife wird abgebrochen wenn alle Objekte aus der Que genommen sind"""
    raw_results = []
    while True:

        queue_value = mp_queue.get()
        if queue_value is None:
            break
        else:
            raw_results.append(queue_value)
            print(queue_value)
    # raw_results = [('38547', 'Bright Light Orange ', 0.3675),
    #                ('38547', 'Orange ', 0.81),
    #                ('38598', 'Bright Light Orange ', 0.3675)]
    results = []

    for i in raw_results:
        filtered = list(filter(lambda a: a.design_id == i[0],results))
        if len(filtered) == 0:
            results.append(BricklinkEinzelteil(i[0], i[1].rstrip(), i[2]))
        else:
            filtered[0].add_color(i[1].rstrip(), i[2])

    for i in results:
        print(i.color_dict)

    p = Process(target=execute_id_translation, args=[results, shop_url, shop_name])
    p.start()
    print(len(raw_results))




