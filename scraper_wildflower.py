import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display

#scraper for wildflower.org
def scrape(name):
    display = Display(visible=0, size=(800, 600))
    display.start()
    image_urls = set()
    driver = webdriver.Chrome()
    driver.get('https://www.wildflower.org/gallery/')
    text_box = driver.find_element_by_id('search_field2')
    go = driver.find_element_by_xpath("//input[@value='go']")
    text_box.send_keys(name)
    go.click()
    time.sleep(1)
    page_div = driver.find_element_by_id('fullpage_content')
    images = page_div.find_elements_by_xpath('//img')
    for image in images[1:]:
        link = image.get_attribute('src').replace('320x240','640x480').replace('160x120','640x480')
        image_urls.add(link)
    driver.close()
    display.stop()
    return image_urls
