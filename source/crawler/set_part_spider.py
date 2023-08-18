import scrapy


class SetPartSpider(scrapy.Spider):
    name = "Part Spider"
    custom_settings = {
        "USER_AGENT": 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    }
    def __init__(self, url, result):
        self.start_url = url
        self.result = result

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""
        url = self.start_url
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for i in response.css(".set"):
            id = i.css(".tags").css("a::text").get()
            qty = i.css(".qty::text").get()
            if qty is not None:
                self.result.append((id, int(qty.replace("x",""))))

        next_url = response.css(".next").css("a::attr(href)").get()
        if next_url is None:
            pass
        else:
            yield scrapy.Request(url=next_url, callback=self.parse)


