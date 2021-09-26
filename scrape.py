from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self, page_url):
        self.driver = webdriver.Firefox()
        self.driver.get(page_url)

    def scrape(self, class_name):
        element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        image = element.screenshot_as_png
        self.__close()
        return image

    def __close(self):
        self.driver.close()
        self.driver.quit()
