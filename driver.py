import scraper_garden
import scraper_wildflower
import scraper_usda
import scraper_google
import concurrent.futures as cf
import os

#meant to collect image links from various sources given a list of scientific names

def add_images(links, scraper, plant, site):
    names = plant.strip().split(',')
    try:
        print('Scraping',site,'for',plant)
        if(site == 'google'):
            links.append((plant, site, scraper(names[0],names[1])))
        else:
            links.append((plant, site, scraper(names[1])))
    except Exception as e:
        print("ERROR WITH ", site, " and plant, ", plant)
        print("Here's the error: ", e)

def scrapers(name):
    link_list = []
    # add_images(link_list, scraper_garden.scrape, name, 'garden')
    add_images(link_list, scraper_wildflower.scrape, name, 'wildflower')
    add_images(link_list, scraper_usda.scrape, name, 'usda')
    add_images(link_list, scraper_google.scrape, name, 'google')
    return link_list

final_list = []
name_file = open('names.csv', 'r')
link_file = open('links.csv', 'w')
executor = cf.ThreadPoolExecutor(max_workers=10)
futures = []

for name in name_file:
    future = executor.submit(scrapers, name)
    futures.append(future)

i = 0
total = len(futures)

for future in cf.as_completed(futures):
    i += 1
    result = future.result()
    for plant, site, links in result:
        for link in links:
            link_file.write(plant.strip()+','+site+','+link+'\n')
    print("Completed ", i, " out of ", total)
    link_file.flush()
    os.fsync(link_file.fileno())

link_file.close()
