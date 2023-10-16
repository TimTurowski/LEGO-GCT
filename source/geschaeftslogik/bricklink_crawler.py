from scrapy.crawler import CrawlerProcess

from source.crawler.teileSpider.teileSpider.spiders.bricklink_spider import BrickLinkSpider


class BricklinkCrawler:

    """crawlt """
    def crawl(self, shop_url, shop_name, category_limit=None):
        process = CrawlerProcess()

        results = []
        process.crawl(BrickLinkSpider, shop_url=shop_url,shop_name=shop_name, result=results, category_limit=category_limit)
        process.start()
        return results


