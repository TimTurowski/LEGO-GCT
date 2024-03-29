import scrapy


class MinifigurSpider(scrapy.Spider):
    name = "Minfigur Spider"
    def __init__(self, url, result):
        self.start_url = url
        self.result = result

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""
        url = self.start_url
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        for i in response.css(".set"):
            qty = i.css(".qty::text").get()
            id = i.css(".tags").css("a::text").get()
            name = i.css(".name::text").get()
            self.result.append((id,name,int(qty[0:len(qty)-1])))