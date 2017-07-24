import scraper_audubon
import scraper_usda
import scraper_google

#meant to collect image links from various sources given a list of scientific names

def add_images(links, scraper,plant, site):
    names = plant.strip().split(',')
    if(site == 'google'):
        links.append((plant, site, scraper(names[0],names[1])))
    else:
        links.append((plant, site, scraper(names[1])))

name_file = open('names.csv', 'r')
link_list = []
for name in name_file:
    # add_images(link_list, scraper_audubon.scrape, name, 'audubon')
    # add_images(link_list, scraper_usda.scrape, name, 'usda')
    add_images(link_list, scraper_google.scrape, name, 'google')
name_file.close()

link_file = open('links.csv', 'w')
for plant, site, links in link_list:
    for link in links:
        link_file.write(plant+','+site+','+link+'\n')
link_file.close()
