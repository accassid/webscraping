from PIL import Image
import io
import requests
import os
import uuid
import time
import multiprocessing as mp

def download(dname, fname, url):
    size = (1024,1024)
    try:
        image_content = requests.get(url).content

    except requests.exceptions.InvalidSchema:
        # image is probably base64 encoded
        image_data = re.sub('^data:image/.+;base64,', '', url)
        image_content = base64.b64decode(image_data)

    except Exception as e:
        print("could not read", e, url)
        return False

    image_file = io.BytesIO(image_content)

    try:
        image = Image.open(image_file).convert('RGB')
        resized = image.resize(size)
        with open(dname+'/'+fname+'.jpg', 'wb') as f:
            resized.save(f, 'JPEG', quality=100)
    except Exception as e:
        print('could not read', e, url)
        return False
    return True

def printsomething():
	i = 0
	while(True):
		print(i)
		i = i+1
		yield

def helper(*args):
    (i, num_lines, line) = args
    # print(i,'/',num_lines)
    split_line = line.split(',')
    dname = 'output/images/'+split_line[1].strip().replace(' ','_')
    fname = str(uuid.uuid4()) + ".jpg"
    url = split_line[3].strip()
    if not os.path.exists(dname):
        os.makedirs(dname, exist_ok=True)
    return download(dname,fname,url)


num_lines = sum(1 for line in open('links.csv')) # is this the best way to do this?
link_file = open('links.csv','r')
pool = mp.Pool(1000)
arglist = []
for i, line in enumerate(link_file):
	arglist.append((i, num_lines, line))
print(len(arglist))
time.sleep(5)
results = pool.starmap(helper, arglist, chunksize=20)
# blocks.
print("Images downloaded: ", len([r for r in results if r]))


