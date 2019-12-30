#
# Scan the file set for missing files. If any file is missing,
# mark the images row in the database with user_delete=2
#
import glob
import os
import sqlite3

conn = sqlite3.connect("danbooru2018_kbr.db")
conn.isolation_level = None
cur = conn.cursor()

base = "G:/original/"
for x in range(1,3368713):
    which = str(x)
    
    # will be contained in a folder modulus 1000, with leading zeros
    fold ='0' + which[-3:]
    while (len(fold) < 4):
        fold = '0' + fold
        
    imagePath = os.path.join(base,fold,which + ".*")
    res = glob.glob(imagePath)
    if len(res) == 0:
        print(which)
        cur.execute('update images set user_delete=2 where image_id=?',(x,))

conn.commit()
conn.close()