# Determine the total file size of all files marked as 
# "complete duplicate" (images.hidden == 4).
#
import sqlite3
import os

# change this to point to the location of your fileset
base = "G:/original/"

conn = sqlite3.connect("danbooru2019.db")
conn.isolation_level = None
cur = conn.cursor()

cur.execute("select image_id,file_ext from images where hidden=4 order by image_id asc")
items = cur.fetchall()

tot_bytes = 0
for item in items:
    image_id = item[0]
    file_ext = item[1]

    fold ='0' + str(image_id)[-3:]
    while (len(fold) < 4):
        fold = '0' + fold

    filename = os.path.join(base, fold, str(image_id) + "." + file_ext)
    print(filename)
    
    try:
        bytes = os.path.getsize(filename)
    except:
        bytes = 0
    tot_bytes += bytes

print("{} ({})".format(str(tot_bytes), str(tot_bytes/1024/1024)))
    
