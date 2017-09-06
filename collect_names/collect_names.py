import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

#Edit these parameters:

zipcode = '14075'

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
last_page = 35 #int(soup.find_all('a', attrs={"data-ng-bind": "resultsC.storage.pager.pager_items.last.page"})[0].get_text())
print(last_page)
driver.close()
names = []
for page_number in range (1, last_page+1):
    url = 'https://www.audubon.org/native-plants/search?zipcode='+zipcode+'&active_tab=full_results&attribute=&attribute_tier1=&resource=&resource_tier1=&bird_type=&bird_type_tier1=&page='+str(page_number)+'&page_tier1=1'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find_all('table')[0]
    scientific_names = table.find_all('em', attrs={"data-ng-bind": "plant.ScientificName"})
    common_names = table.find_all('label', attrs={"data-ng-bind": "plant.CommonName"})
    print('Page:',page_number)
    print(len(scientific_names))
    print(len(common_names))
    for x in range(0, len(scientific_names)):
        names.append((common_names[x].get_text(), scientific_names[x].get_text()))
    driver.close()

output = open(zipcode+time.strftime("-%Y-%m-%d-%H:%M:%S.csv"), 'w')
for common_name, scientific_name in names:
    output.write(common_name+','+scientific_name+'\n')

output.close()
