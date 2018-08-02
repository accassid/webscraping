# Image Web Scraper and Classifier

This project was designed for the purpose of from a list of plants with their common and scientific names, to download a sampleset of images for each plant in the list and train a CNN for the purpose of identifying those plants.

##Web Scraper
###Scraping and downloading from a list of names
The main entrypoint to the webscrapping app is through `driver.py`. Running `python driver.py` will  open a predetermined list of plant names in `names.csv` the format "Common Name,Scientific name". It will then go through four different web sources of plant imagery (one of which being google images) and save image links to a file called `links.csv`. This links can then be downloaded by running `python downloader.py`. Within `downloader.py` you can set the `size` variable to the desired size in pixles that all the downloaded images will be sized to (the majority of image classification algorithms will require equally sized images).
###Obtaining a list of names
In the `collect_names` directory, a list of plants native to a zipcode can be obtained by runing `python collect_names.py`. The results will be stored in `names.csv` which can be used for the scraper. Modify the `zipcode` variable in `collect_names.py` to collect names from your desired zipcode.

##Image Classifier
The main entrypoint into the image classification app is through `tfscript.py`. Running this will already assume you have results stored in the `output` directory from the downloader script. Running `python tfscript.py` will pass the images through a convolutional neural network and then test the network on a random subset of images and report accuracy.
