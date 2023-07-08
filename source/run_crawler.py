from source.crawler import LegoCrawler
from source.datastructures.einzelteil import Einzelteil

crawler = LegoCrawler()
results = crawler.crawl_preis([Einzelteil("6438899"), Einzelteil("6359941")])

for i in results.get_lego_teile():
    print("id:",i.einzelteil.element_id,"preis:",i.preis,"url:", i.url)
results = crawler.crawl_preis([Einzelteil("6438899"), Einzelteil("6359941")])

for i in results.get_lego_teile():
    print("id:",i.einzelteil.element_id,"preis:",i.preis,"url:", i.url)
