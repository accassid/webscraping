from PIL import Image
import io
import requests
import os
import uuid
import time
import concurrent.futures as cf

def download(dname, fname, url):
    size = (1024,1024)
    try:
        image_content = requests.get(url).content

    except requests.exceptions.ConnectionError:
        print("ConnectionError, sleeping then trying again.")
        time.sleep(5)
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

def helper(arglist):

    for args in arglist:

        (i, num_lines, line) = args
        print(i,'/',num_lines)
        split_line = line.split(',')
        dname = "/mnt/external/images/"+split_line[1].strip().replace(' ','_')
        fname = str(uuid.uuid4())
        url = split_line[3].strip()
        if not os.path.exists(dname):
            os.makedirs(dname, exist_ok=True)
        try:
            download(dname,fname,url)
        except:
            print("Exception, didn't download")
    return True


num_lines = sum(1 for line in open('links.csv')) # is this the best way to do this?
link_file = open('links.csv','r')
executor = cf.ThreadPoolExecutor(max_workers=1000)
arglist = []
for i, line in enumerate(link_file):
    arglist.append((i, num_lines, line))
num_images = len(arglist)
num_thread = 1000
im_per_thread = int(num_images / num_thread)
print("This many images per thread:", im_per_thread)
futures = []
for k in range(num_thread):
    start = k*im_per_thread
    end = (k+1)*im_per_thread
    future = executor.submit(helper, arglist[start:end])
    futures.append(future)

for future in cf.as_completed(futures):
    print("Thread finished.")

print("Done.")


