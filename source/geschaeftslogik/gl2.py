import multiprocessing
from multiprocessing import Process

from source.crawler.part_crawler import PartCrawler

def execute_crawling(set_id,set_name, part_crawler, conn2):
    crawler = part_crawler
    crawl_result = crawler.crawl_set_parts(set_id, set_name)
    print(crawl_result)
    conn2.send("crawl_result.stueckliste")


if __name__ == "__main__":
    conn1, conn2 = multiprocessing.Pipe()
    """erstellt Prozess in welchem der Crawl vorgang gestartet wird dies ermöglicht mehrere Crawl vorgänge"""
    p = Process(target=execute_crawling, args=("21007","Rockefeller Plaza", PartCrawler(), conn2))
    p.start()
    p.join()
    stueckliste = conn1.recv()
    print("test")
    # print(stueckliste)

    # print(part_crawler.crawl_set_parts("10155", "Maersk Line City"))