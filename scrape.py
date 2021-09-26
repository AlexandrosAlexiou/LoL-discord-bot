from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class Scraper:
    def __init__(self, page_url):
        options = Options()
        options.headless = True
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(page_url)

    def scrape(self, class_name=None, xpath=None):
        if class_name:
            element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        if xpath:
            element = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath)))
        image = element.screenshot_as_png
        self.__close()
        return image

    def __close(self):
        self.driver.close()
        self.driver.quit()
