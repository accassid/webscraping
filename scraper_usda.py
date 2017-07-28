import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from pyvirtualdisplay import Display

#scraper for plants.usda
def scrape(name):
    display = Display(visible=0, size=(800, 600))
    display.start()
    image_urls = set()
    driver = webdriver.Chrome()
    driver.get('https://plants.usda.gov/java/')
    search_box = driver.find_element_by_id('searchtext')
    search_button = driver.find_element_by_id('submit')
    search_box.send_keys(name)
    search_button.click()
    time.sleep(2)
    if 'nameSearch' in driver.current_url:
        table = driver.find_element_by_xpath("//table[@summary='PLANTS Name Search Results']")
        td = table.find_element_by_xpath("//td")
        link = td.find_element_by_xpath("//a")
        em = link.find_element_by_xpath("//em")
        em.click()
        time.sleep(1)
    image_link = driver.find_element_by_xpath("//a[@title='click to view all images for this plant']")
    image_link.click()
    time.sleep(1)
    count = 0
    aa = driver.find_elements_by_xpath("//a[@title='click to view a large image']")
    for a in aa:
        link = a.get_attribute('href')
        full_image_link = 'https://plants.usda.gov/gallery/pubs/'+link.split('=')[1][:-7]+link.split('=')[1][-7:].replace('a','p').replace('tif','jpg')
        if not 'pvp' in full_image_link and not 'php' in full_image_link and not 'pvd' in full_image_link:
            print('not a full image?')
            print(link)
        else:
            image_urls.add(full_image_link)
            # print(full_image_link)
    driver.close()
    display.stop()
    return image_urls
