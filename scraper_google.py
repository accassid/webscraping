import os
import re
import time
import requests
import io
import hashlib
import itertools
import base64
import json
from PIL import Image
from multiprocessing import Pool
from selenium import webdriver


def scrape(common_name, scientific_name):
    link_set = set()
    link_set.update(scraper_helper(common_name))
    link_set.update(scraper_helper(common_name+' leaf'))
    link_set.update(scraper_helper(scientific_name))
    link_set.update(scraper_helper(scientific_name+' leaf'))
    return link_set

def scraper_helper(query, images_to_download=20):
	image_urls = set()
	search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
	caps = webdriver.DesiredCapabilities().FIREFOX
	caps["marionette"] = False
	browser = webdriver.Chrome()
	browser.get(search_url.format(q=query))
	def scroll_to_bottom():
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)

	image_count = len(image_urls)
	delta = 0
	while image_count < images_to_download:
		print("Found:", len(image_urls), "images")
		scroll_to_bottom()
		images = browser.find_elements_by_class_name("rg_meta")
		for img in images:
			json_text = img.get_attribute("innerText")
			json_obj = json.loads(json_text)
			image_urls.add(json_obj["ou"])

		delta = len(image_urls) - image_count
		image_count = len(image_urls)

		if delta == 0:
			print("Can't find more images")
			break

		fetch_more_button = browser.find_element_by_css_selector(".ksb._kvc")
		if fetch_more_button:
			browser.execute_script("document.querySelector('.ksb._kvc').click();")
			scroll_to_bottom()

	browser.quit()
	return image_urls
