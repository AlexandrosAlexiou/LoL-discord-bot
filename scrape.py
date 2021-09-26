from selenium import webdriver
from PIL import Image
from io import BytesIO
import time

fox = webdriver.Firefox()
fox.get('https://u.gg/lol/champions/aatrox/build')
time.sleep(3)
# now that we have the preliminary stuff out of the way time to get that image :D
element = fox.find_element_by_class_name("champion-profile-content-container")
# click screenshot
element.screenshot('aatrox.png')
fox.close()
fox.quit()