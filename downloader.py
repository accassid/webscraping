from PIL import Image
import io
import requests
import os
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

def helper(i,num_lines,line):
    print(i,'/',num_lines)
    split_line = line.split(',')
    dname = 'output/images/'+split_line[1].strip().replace(' ','_')
    fname = split_line[2]+str(i)
    url = split_line[3].strip()
    if not os.path.exists(dname):
        os.makedirs(dname)
    return download(dname,fname,url)

def read_file():
    num_lines = sum(1 for line in open('links.csv'))
    link_file = open('links.csv','r')
    cpu_count = mp.cpu_count()
    pool = mp.Pool(processes=cpu_count)
    results = [pool.apply_async(helper,args=(i,num_lines,line,)) for i, line in enumerate(link_file)]
    output = [p.get() for p in results]




read_file()
# download('output/images/Asclepias_tuberosa', 'usda', 'https://plants.usda.gov/gallery/pubs/rual_003_pvp.jpg')
