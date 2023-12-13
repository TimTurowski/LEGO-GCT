import scrapy

class MinifigurPartSpider(scrapy.Spider):
    name = "Part Spider"
    def __init__(self, url, result):
        self.start_url = url
        self.result = result

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""
        url = self.start_url
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for i in response.css(".set"):
            item = i.css(".tags").css("a::text").get()
            # print(i.css(".meta").css("a::text").get().lstrip())
            # print(item)
            # if i.css(".subtheme::text").get() != "Technic":
            self.result.append((item, i.css(".meta").css("a::text").get().lstrip()))

        next_url = response.css(".next").css("a::attr(href)").get()
        if next_url is None:
            pass
        else:
            yield scrapy.Request(url=next_url, callback=self.parse)