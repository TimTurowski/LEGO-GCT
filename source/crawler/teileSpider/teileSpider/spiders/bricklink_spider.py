import scrapy
from scrapy_selenium import SeleniumRequest
import time
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver


# scrapy runspider bricklink_spider.py

class BrickLinkSpider(scrapy.Spider):
    name = "bricklink"
    custom_settings = {

        "LOG_ENABLED": False,
        "USER_AGENT": 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    }

    def start_requests(self):

        # url = "http://httpbin.org/ip"
        url = "https://store.bricklink.com/generationbrick?p=generationbrick#/shop?o={%22itemType%22:%22P%22,%22catID%22:%223%22,%22showHomeItems%22:0}"
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=10000)

    def parse(self, response):
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.get(
            "https://store.bricklink.com/generationbrick?p=generationbrick#/shop?o={%22itemType%22:%22P%22,%22catID%22:%223%22,%22showHomeItems%22:0}")

        time.sleep(1)
        categories = driver.find_element(By.XPATH,
                                         "/html/body/div[2]/div[3]/div/aside/div/div/div[2]/section/div/div[2]/div[2]/div/div[1]") \
            .find_elements(By.CSS_SELECTOR, "a")
        parts = []
        """Iterieren über die Kategorien"""
        for i in categories[0:6]:
            i.click()
            time.sleep(1)

            """Auflösen der Seitenanzahl"""
            page_count = int(driver.find_element(By.CLASS_NAME, "pagination").text.splitlines()[-2])


            """Iterieren über die EinzelTeileseiten"""
            for page in range(0, page_count):

                button = driver.find_element(By.CSS_SELECTOR, "	[aria-label='Next']")
                button.click()
                time.sleep(1)
                for article_element in driver.find_elements(By.CSS_SELECTOR, "article"):
                    color = article_element.find_element(By.CLASS_NAME, "description") \
                        .find_element(By.CSS_SELECTOR, "strong").text

                    desing_id = article_element.find_element(By.CLASS_NAME, "bl-breadcrumb") \
                        .find_elements(By.CSS_SELECTOR, "a")[-1].text

                    price = float(article_element.find_element(By.CLASS_NAME, "buy") \
                                  .find_elements(By.CSS_SELECTOR, "strong")[-1].text.replace("EUR ", ""))
                    # print(price)
                    parts.append([desing_id, color, price])

        """schreiben der CSV Datei mit den Einzelteilen"""
        with open("parts.csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for i in parts:
                writer.writerow(i)
