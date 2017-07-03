import os
import scraper_audubon
import scraper_usda

#meant to collect image links from various sources given a list of scientific names

def add_images(links, scraper):
    links.append('hullo')

name_file = open('names.txt', 'r')
link_list = []

add_images(link_list, scraper_audubon.scrape)
add_images(link_list, scraper_usda.scrape)
print(links(len))


name_file.close()
