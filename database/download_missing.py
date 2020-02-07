# For every file marked as "missing" in the database,
# attempt to download the file directly from danbooru.
#
# A file may be "missing" because it requires a "gold account"
# to view. In that case, the data downloaded for the post
# will be missing a "file_url" value.
#
# Files are downloaded to a folder structure that matches
# Gwent's structure (in the current directory).
#
# For politeness, there is a one minute delay after downloading
# a file.
#

import requests
import json
import sqlite3
import time
import os

base = "https://danbooru.donmai.us/posts/"

conn = sqlite3.connect("../danbooru2019.db")
conn.isolation_level = None
cur = conn.cursor()

# fetch all image info where marked as 'missing'
# TODO doesn't take into account (non-image)+(missing) and other flag combos
last = 0
cur.execute("select image_id,file_ext from images where hidden=2 and image_id > ? order by image_id asc",(last,))
items = cur.fetchall()

for item in items:
    image_id = item[0]
    file_ext = item[1]
    
    print(image_id)
    
    url = base + str(image_id) + ".json"
    response = requests.get(url)
    if response.status_code != 200:
        print("Danbooru fail:" + str(response.status_code))
        exit()
        
    respj = response.json()
    #print(respj)

    # If the post has a file_url, it can be downloaded
    # A post may not have a file_url (e.g. requires a gold account). 
    # So far, attempting to use the 'source' URL has always failed.

    if 'file_url' in respj:
        print(respj['file_url'])
        image_url = respj['file_url']
    elif 'source' in respj:
        print("Source URL: not used")
        continue
    else:
        print('No URL')
        continue
    
    r = requests.get(image_url)
    if r.status_code != 200:
        print("Image download fail!")
        continue

    # place the image in the appropriate subfolder
    fold ='0' + str(image_id)[-3:]
    while (len(fold) < 4):
        fold = '0' + fold
    if not os.path.isdir(fold):
        os.makedirs(fold)
    
    # use file_ext from database
    filename = os.path.join(fold, str(image_id) + "." + file_ext)
    with open(filename, 'wb') as f:
        f.write(r.content)

    time.sleep(60)
