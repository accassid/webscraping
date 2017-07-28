import requests
from bs4 import BeautifulSoup

#scraper for garden.org
def scrape(name):
    image_urls = set()
    page = requests.get('https://garden.org/plants/search/text.php?q='+name.split(' ')[0]+'+'+name.split(' ')[1])
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('tbody')
    boxes = table.find_all('a')
    a = boxes[0]
    #check for entry that contains only the desired scientific name
    for box in boxes:
        if '('+name+')' in box.get_text():
            a = box
    page = requests.get('https://garden.org'+a['href'])
    soup = BeautifulSoup(page.content, 'html.parser')
    for box in soup.find_all('div', class_='plant_thumbbox'):
        image = box.find('img')
        image_link = 'https://garden.org'+image['src'].replace('-175','')
        # print(image_link)
        image_urls.add(image_link)
    return image_urls
