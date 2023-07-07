import unittest
from source.datastructures.einzelteil import Einzelteil
from source.crawler.lego_crawler import LegoCrawler

class MyTest(unittest.TestCase):
    def test_valides_einzelteil(self):
        crawler = LegoCrawler()
        result = crawler.crawl_preis([Einzelteil("300526")])

        marktpreis = result.get_lego_teile()[0]
        self.assertEqual(marktpreis.einzelteil.element_id, "300526")
        self.assertEqual(marktpreis.preis, 0.07)
        self.assertEqual(marktpreis.url, "https://www.lego.com/de-de/pick-and-build/pick-a-brick?query=300526")




if __name__ == '__main__':
    unittest.main()


