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
    cur.execute('select image_id from images where image_id > ? order by image_id limit 10000',(last,))
    res = cur.fetchall()
    if len(res) == 0: # no more, we're done
        exit()
    
    for id in [i[0] for i in res]:
        which = str(id)
        
        # will be contained in a folder modulus 1000, with leading zeros
        fold ='0' + which[-3:]
        while (len(fold) < 4):
            fold = '0' + fold

        # TODO this may be a slow variant of exists(), is there a faster way?
        imagePath = os.path.join(base,fold,which + ".*")
        res1 = glob.glob(imagePath)
        imagePath2 = os.path.join(base2,fold,which + ".*")
        res2 = glob.glob(imagePath2)
        if len(res1) == 0 and len(res2)==0:
            print(which)
            # mark the image as 'missing' in the database
            cur.execute('update images set hidden=2 where image_id=?',(id,))
        
    last = res[len(res)-1][0]
    print("#-" + str(last))
    if (last > 3734659): # fileset stops at 3734659, we're done
        exit()
