import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import logging

logging.basicConfig(level=logging.NOTSET)


class Scraper:
    def __init__(self):
        options = Options()
        options.headless = True
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-gpu')
        production = os.getenv('PRODUCTION') or os.environ.get("PRODUCTION")
        if production == 'false':
            self.driver = webdriver.Firefox(options=options)
        else:
            self.driver = webdriver.Firefox(options=options,
                                            executable_path=os.environ.get(
                                                "GECKODRIVER_PATH"),
                                            firefox_binary=FirefoxBinary(os.environ.get("FIREFOX_BIN")))

    def scrape(self, page_url=None, class_name=None):
        logging.info(
            f"[Hippalus Scraper] Scraping: {page_url} for classname: {class_name}")
        self.driver.get(page_url)
        element = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        image = element.screenshot_as_png
        return image

    def close(self):
        self.driver.close()
        self.driver.quit()
