# For each image listed in the metadata, determine if the physical
# file exists.
# 
import sqlite3
import os
import glob

conn = sqlite3.connect("danbooru2019.db")
conn.isolation_level = None
cur = conn.cursor()

# In my copy of the fileset, I've split the files into "images" and
# "non-images". These are the base directories for those two groups.
base = "G:/original/"
base2 = "E:/proj/danbooru2018/non_image/"

last = 0

# process images in batches of 10000
while True:
    cur.execute('select image_id,file_ext from images where image_id > ? order by image_id limit 10000',(last,))
    res = cur.fetchall()
    if len(res) == 0: # no more, we're done
        exit()
    
    for tup in res:
        id = tup[0]
        ext = tup[1]
        which = str(id)
        
        # will be contained in a folder modulus 1000, with leading zeros
        fold ='0' + which[-3:]
        while (len(fold) < 4):
            fold = '0' + fold

        imagePath = os.path.join(base,fold,which + "." + ext)
        if not os.path.isfile(imagePath):
            imagePath2 = os.path.join(base2,fold,which + "." + ext)
            if not os.path.isfile(imagePath2):
                print(which)
                # TODO replace with "update images set hidden=(select hidden from images where image_id=1) | 2 where image_id=1"
                # mark the image as 'missing' in the database
                cur.execute("select hidden from images where image_id=?",(id,))
                val = cur.fetchall()[0][0]
                cur.execute('update images set hidden=? where image_id=?',((val | 2),id))
        
    last = res[len(res)-1][0]
    print("#-" + str(last))
    if (last > 3734659): # fileset stops at 3734659, we're done
        exit()
