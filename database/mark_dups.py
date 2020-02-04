# given a file of dup paths
# mark said image id as dup IFF provided extension matches database
#
# Assumes a text file containing one file path per line, where each
# indicates a file has been identified as a duplication. Assumed to 
# be a complete file path, e.g. G:\original\0201\708201.png
#
import os
import sys
import sqlite3

conn = sqlite3.connect("..\danbooru2019.db")
conn.isolation_level = None
cur = conn.cursor()

with open(sys.argv[1]) as f:
    lines = f.readlines()
    
for line in lines:
    _,fname = os.path.split(line.strip())
    image_id,ext = os.path.splitext(fname)
    ext = ext[1:]

    # TODO replace with "update images set hidden=(select hidden from images where image_id=1) | 2 where image_id=1"
    cur.execute('select image_id, hidden from images where image_id=? and file_ext=?',
                (image_id,ext))
    res = cur.fetchall()
    if len(res) != 0:
        print(res[0][1])
        val = res[0][1] | 4
        print(val)
        cur.execute('update images set hidden=? where image_id=?',
                (val,image_id))

conn.close()
