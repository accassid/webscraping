import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

#Edit these parameters:

zipcode = '14051'

#scraper


#get number of pages
url = 'https://www.audubon.org/native-plants/search?zipcode='+zipcode+'&active_tab=full_results&attribute=&attribute_tier1=&resource=&resource_tier1=&bird_type=&bird_type_tier1=&page=1&page_tier1=1'
driver = webdriver.Chrome()
# driver.set_window_position(-1000000,0)
# driver.set_window_size(0, 0)
driver.get(url)
time.sleep(1)
# page1 = requests.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
last_page = int(soup.find_all('a', attrs={"data-ng-bind": "resultsC.storage.pager.pager_items.last.page"})[0].get_text())
print(last_page)
driver.close()
scientific_names = []
for page_number in range (1, last_page+1):
    url = 'https://www.audubon.org/native-plants/search?zipcode='+zipcode+'&active_tab=full_results&attribute=&attribute_tier1=&resource=&resource_tier1=&bird_type=&bird_type_tier1=&page='+str(page_number)+'&page_tier1=1'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find_all('table')[0]
    names = table.find_all('em', attrs={"data-ng-bind": "plant.ScientificName"})
    print('Page:',page_number)
    print(len(names))
    for name in names:
        scientific_names.append(name.get_text())
    driver.close()

output = open(zipcode+time.strftime("-%Y-%m-%d-%H:%M:%S.csv"), 'w')
for name in scientific_names:
    output.write(name+'\n')

output.close()
