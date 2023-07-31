import multiprocessing
import unittest
from multiprocessing import Process
from source.Entity.entities import Einzelteil
from source.crawler.lego_crawler import LegoCrawler


def execute_crawling(einzelteile, teile_crawler, conn2):
    crawler = teile_crawler
    result = crawler.crawl_preis(einzelteile)
    """gibt informationen über den Crawl vorgang aus"""
    conn2.send(result)

class MyTest(unittest.TestCase):

    def test_valides_einzelteil(self):
        """referenz Dictonary zum abgleichen der Preise mit den Preisen des Crawl results. Stand 30.07.2023"""
        reference_dict = {"6435857": 0.14,
                          "6406522": 0.33,
                          "6411329": 0.1,
                          "6390506": 1.59}

        sample_einzelteile = [Einzelteil(einzelteil_id="6435857"),
                              Einzelteil(einzelteil_id="6406522"),
                              Einzelteil(einzelteil_id="6411329"),
                              Einzelteil(einzelteil_id="6390506"),
                              Einzelteil(einzelteil_id="6360899")]

        conn1, conn2 = multiprocessing.Pipe()
        p = Process(target=execute_crawling, args=(sample_einzelteile, LegoCrawler(), conn2))
        p.start()
        p.join()
        lego_crawl_result = conn1.recv()
        marktpreise = lego_crawl_result.einzelteil_marktpreise

        """generiert aus Liste von marktpreisen ein Dict"""
        result_dict = {}
        for i in marktpreise:
            result_dict[i.einzelteile.einzelteil_id] = i.preis

        self.assertEqual(reference_dict, result_dict)


if __name__ == '__main__':
    unittest.main()



