import scraper_garden
import scraper_wildflower
import scraper_usda
import scraper_google
import concurrent.futures as cf

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
executor = cf.ThreadPoolExecutor(max_workers=400)
futures = []

for name in name_file:
    future = executor.submit(scrapers, name)
    futures.append(future)

i = 0
total = len(futures)

for future in cf.as_completed(futures):
    print("Completed ", i, " out of ", total)
    i += 1
    final_list.extend(future.result())

link_file = open('links.csv', 'w')
for plant, site, links in final_list:
    for link in links:
        link_file.write(plant.strip()+','+site+','+link+'\n')
link_file.close()
