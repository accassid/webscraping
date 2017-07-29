import scraper_garden
import scraper_wildflower
import scraper_usda
import scraper_google
import multiprocessing as mp

#meant to collect image links from various sources given a list of scientific names

def add_images(links, scraper,plant, site):
    names = plant.strip().split(',')
    try:
        print('Scraping',site,'for',plant)
        if(site == 'google'):
            links.append((plant, site, scraper(names[0],names[1])))
        else:
            links.append((plant, site, scraper(names[1])))
    except:
        print('ERROR WITH',site,'and plant,',plant)

def scrapers(name):
    link_list = []
    add_images(link_list, scraper_garden.scrape, name, 'garden')
    add_images(link_list, scraper_wildflower.scrape, name, 'wildflower')
    add_images(link_list, scraper_usda.scrape, name, 'usda')
    add_images(link_list, scraper_google.scrape, name, 'google')
    return link_list

cpu_count = mp.cpu_count()
final_list = []
name_file = open('names.csv', 'r')
pool = mp.Pool(processes=cpu_count)
results = [pool.apply_async(scrapers,args=(name,)) for name in name_file]
for p in results:
    final_list.extend(p.get())

name_file.close()
link_file = open('links.csv', 'w')
for plant, site, links in final_list:
    for link in links:
        link_file.write(plant.strip()+','+site+','+link+'\n')
link_file.close()
