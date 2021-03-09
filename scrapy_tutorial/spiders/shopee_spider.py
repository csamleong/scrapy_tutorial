import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger


class QuotesSpider(scrapy.Spider):
    name = "shopee"

    def start_requests(self):
        urls = [
            'https://shopee.tw/flash_sale'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # to handle url array
        page = response.url.split("/")[-2]

        filename = f'shopee-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        # driver = webdriver.Chrome()  # To open a new browser window and navigate it

        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

        # Getting list of Countries
        driver.get(response.url)

        # Implicit wait
        driver.implicitly_wait(10)

        # Explicit wait
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "flash-sale-items")))

        # Extracting country names
        countries = driver.find_elements_by_class_name("flash-sale-items")
        countries_count = 0
        # Using Scrapy's yield to store output instead of explicitly writing to a JSON file
        for country in countries:
            yield {
                "country": country.text,
            }
            countries_count += 1

        driver.quit()
        logger.info(
            f"Total number of Countries in openaq.org: {countries_count}")
