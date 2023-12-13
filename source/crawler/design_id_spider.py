import scrapy

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
              "Medium Lavender": "Medium Lavender"
              }
reversed_color_dict = dict((v, k) for k, v in color_dict.items());


class DesignIdSpider(scrapy.Spider):
    name = "Design Id Spider"

    def __init__(self, brickset_url, toypro_url, result, values):
        self.brickset_url = brickset_url
        self.toypro_url = toypro_url

        self.result = result
        # self.element_id = values[0];
        self.values = values;
        # self.colors = list(self.prices.keys());

    def start_requests(self):
        """Seite hat informationen über Lego sets und verweist auf Lego set anleitungen"""
        for i in self.values:

            if i[0].isdigit():
                url = self.brickset_url + "query=" + i[0]
                yield scrapy.Request(url=url, callback=self.parse_brickset, cb_kwargs={"prices": i[1], "colors": list(i[1].keys())})
            else:
                url = self.toypro_url + "search=" + i[0]
                yield scrapy.Request(url=url, callback=self.parse_toypro,
                                     cb_kwargs={"prices": i[1], "bricklink_id": i[0]})

    def parse_brickset(self, response, prices, colors):
        """parst eine Brickset Seite auswertung von Numerischer ID mit Farbcode
        über die Seite von Brickset"""
        regex = ""
        for i in colors:
            try:
                regex = regex + color_dict[i] + "|"
            except:
                regex = regex + i + "|"

        regex = regex[:-1]
        for i in response.css(".set"):
            """/html/body/div[2]/div/div/section/article[8]/div[2]/div[1]/a[6]"""
            if len(i.re(r"" + regex)) > 0:
                color = i.xpath("div[2]/div[1]/a[6]/text()").get();
                price = prices[reversed_color_dict[color]]
                element_id = i.css(".tags").css("a::text").get()
                self.result.append((element_id, color, price))

    def parse_toypro(self, response, prices, bricklink_id):
        """wenn die Id nicht ausschließlich aus Zahlen besteht, dann wird über toypro
        versucht die Id in eine Lego Element Id umzusetzen"""
        item_page = response.xpath("/html/body/main/div[4]/div[1]/div/a").css("a::attr(href)").get()
        yield scrapy.Request(url="https://www.toypro.com" + item_page,
                             callback=self.parse_toypro_item_page,
                             cb_kwargs={"prices": prices, "bricklink_id": bricklink_id})

    def parse_toypro_item_page(self, response, prices, bricklink_id):
        """Liest eine Shop Seite aus und überprüft die Elementid des Teils auf richtigkeit"""

        """holt die Bricklink id von der Toypro seite (HTML Tags und Bezeichnung werden abgeschnitten)"""
        try:
            parsed_bricklink_id = response.xpath("/html/body/main/div[2]/div/div/div/div[2]/div[1]/div[1]/div/ul")\
                .re("LEGO® Design ID: .*")[0][17:-5]
            element_id = response.xpath("/html/body/main/div[2]/div/div/div/div[2]/div[1]/div[1]/div/ul")\
                .re("LEGO® Element ID: .*")[0][18:-5]

            if parsed_bricklink_id == bricklink_id:
                self.result.append((element_id, None, list(prices.values())[0]))
        except:
            print("Keine Element Id zur gegebenen Design Id vorhanden")
