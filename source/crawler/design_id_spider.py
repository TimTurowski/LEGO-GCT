import scrapy
from scrapy.crawler import CrawlerProcess

color_dict = {"Aqua": "Light Bluish Green",
              "Black": "Black",
              "Blue": "Bright Blue",
              "Bright Green": "Bright Green",
              "Bright Light Orange": "Flame Yellowish Orange",
              "Light Purple": "Bright Reddish Lilac",
              "Chrome Silver": "Silver",
              "Trans-Clear": "Transparent",
              "Glitter Trans-Clear": "Transparent Glitter",
              "Bright Light Yellow": "Cool Yellow",
              "Dark Azure": "Dark Azur",
              "Dark Brown": "Dark Brown",
              "Dark Flesh": "Brown",
              "Dark Green": "Earth Green",
              "Dark Orange": "Dark Orange",
              "Dark Pink": "Bright Purple",
              "Dark Red": "Dark Red",
              "Dark Blue-Violet": "Dark Royal Blue",
              "Dark Bluish Gray": "Dark Stone Grey",
              "Dark Tan": "Sand Yellow",
              "Sky Blue": "Dove Blue",
              "Medium Dark Pink": "Medium Reddish Violet",
              "Earth Orange": "Light Orange Brown",
              "Flesh": "Nougat",
              "Glow In Dark Opaque": "Phosp. White",
              "Green": "Dark Green",
              "Lime": "Br. Yellowish Green",
              "Light Aqua": "Aqua",
              "Light Blue": "Light Blue",
              "Light Flesh": "Light Nougat",
              "Light Green": "Light Green",
              "Light Lime": "Lig. Yellowish Green",
              "Light Orange": "Light Orange",
              "Bright Pink": "Light Purple",
              "Bright Light Blue": "Light Royal Blue",
              "Light Salmon": "Light Red",
              "Very Light Bluish Gray": "Light Stone Grey",
              "Light Turquoise": "Med. Bluish Green",
              "Light Violet": "Light Bluish Violet",
              "Light Yellow": "Light Yellow",
              "Maersk Blue": "Pastel Blue",
              "Magenta": "Bright Reddish Violet",
              "Medium Blue": "Medium Blue",
              "Medium Dark Flesh": "Medium Nougat",
              "Medium Green": "Medium Green",
              "Dark Purple": "Medium Lilac",
              "Medium Lime": "Med. Yellowish Green",
              "Medium Orange": "Br. Yellowish Orange",
              "Light Bluish Gray": "Medium Stone Grey",
              "Metallic Green": "Lemon Metallic",
              "Dark Blue": "Earth Blue",
              "Brown": "Earth Orange",
              "Dark Gray": "Dark Grey",
              "Light Gray": "Grey",
              "Orange": "Bright Orange",
              "Very Light Orange": "Light Yellowish Orange",
              "Light Pink": "Light Pink",
              "Metal Blue": "Sand Blue Metallic",
              "Copper": "Copper",
              "Flat Dark Gold": "Sand Yellow Metallic",
              "Pearl Dark Gray": "Metallic Dark Grey",
              "Pearl Gold": "Warm Gold",
              "Pearl Light Gold": "Gold",
              "Pearl Light Gray": "Silver",
              "Flat Silver": "Silver flip/flop",
              "Pink": "Pink",
              "Purple": "Bright Violet",
              "Red": "Bright Red",
              "Reddish Brown": "Reddish Brown",
              "Blue-Violet": "Medium Bluish Violet",
              "Rust": "Rust",
              "Salmon": "Brick Red",
              "Sand Blue": "Sand Blue",
              "Sand Green": "Sand Green",
              "Sand Purple": "Sand Violet",
              "Sand Red": "Sand Red",
              "Very Light Gray": "Light Grey",
              "Trans-Black": "Tr. Brown",
              "Tan": "Brick Yellow",
              "Dark Turquoise": "Bright Bluish Green",
              "Trans-Dark Blue": "Tr. Blue",
              "Trans-Bright Green": "Transparent Bright Green",
              "Trans-Orange": "Tr. Bright Orange",
              "Glow In Dark Trans": "Phosh. Green",
              "Trans-Green": "Tr. Green",
              "Trans-Light Blue": "Tr. Lg Blue",
              "Milky White": "Nature",
              "Trans-Medium Blue": "Tr. Flu. Blue",
              "Trans-Neon Green": "Tr. Flu. Green",
              "Trans-Neon Orange": "Tr. Flu. Reddish orange",
              "Trans-Neon Yellow": "Transparent Fluorescent Yellow",
              "Trans-Dark Pink": "Tr. Medi. Reddish violet",
              "Glitter Trans-Dark Pink": "Tr. Medium Reddish-Violet w. Glitter 2%",
              "Trans-Purple": "Tr. Bright Bluish Violet",
              "Glitter Trans-Purple": "Tr. B:right Bluish Violet w. Glitter 2%",
              "Trans-Red": "Tr. Red",
              "Trans-Yellow": "Tr. Yellow",
              "Violet": "Bright Bluish Violet",
              "White": "White",
              "Yellow": "Bright Yellow",
              }
reversed_color_dict = dict((v, k) for k, v in color_dict.items());


class DesignIdSpider(scrapy.Spider):
    name = "Design Id Spider"

    def __init__(self, url, result, values):
        self.start_url = url
        self.result = result
        # self.element_id = values[0];
        self.values = values;
        # self.colors = list(self.prices.keys());

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""
        for i in self.values:
            url = self.start_url + "query=" + i[0]
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={"prices": i[1], "colors": list(i[1].keys())})

    def parse(self, response, prices, colors):
        regex = ""
        for i in colors:
            regex = regex + color_dict[i] + "|"

        regex = regex[:-1]
        for i in response.css(".set"):
            """/html/body/div[2]/div/div/section/article[8]/div[2]/div[1]/a[6]"""
            if len(i.re(r"" + regex)) > 0:
                color = i.xpath("div[2]/div[1]/a[6]/text()").get();
                price = prices[reversed_color_dict[color]]
                element_id = i.css(".tags").css("a::text").get()
                self.result.append((element_id, color, price))
                # print(i.css(".tags").css("a::text").get()+" "+ color +" " + str(prices[reversed_color_dict[color]]));
