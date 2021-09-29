import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv


class Scraper:
    def __init__(self, page_url):
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
                                            executable_path=os.environ.get("GECKODRIVER_PATH"),
                                            firefox_binary=FirefoxBinary(os.environ.get("FIREFOX_BIN")))
        self.driver.get(page_url)

    def scrape(self, class_name=None, xpath=None):
        try:
            WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.CLASS_NAME, 'css-1litn2c'))).click()
        except TimeoutException:
            pass
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
