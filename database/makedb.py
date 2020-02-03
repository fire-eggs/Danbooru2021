# Based on https://github.com/jxu/danbooru2018-metadata/blob/master/read_json.py
# Modified slightly for db2019:
# - do not track danbooru favorites
# - do not track danbooru pools
# - change 'user_delete' to 'hidden'
#
# The 'hidden' column is used to hide files from the browser. It is a set
# of flags, with the current values:
# 0 : not hidden
# 1 : user has marked as hidden
# 2 : file is missing
# 4 : file is a 'pure' duplication of another file
# 8 : file is an 'effective' duplication of another file [different in size/encoding]
# 16: file is not an image (rar,zip,swf,mp4,webm,mpg,etc)
#

import sqlite3
import json
import os

# json files are in the following folder
DATA_DIR = "metadata"

def main():
    conn = sqlite3.connect("danbooru2019.db")
    c = conn.cursor()

    # note: keys do not exactly match columns in db
    images_keys = ("id",
                   "created_at",
                   "uploader_id",
                   "score",
                   "source",
                   "md5",
                   "last_commented_at",
                   "rating",
                   "image_width",
                   "image_height",
                   "is_note_locked",
                   "file_ext",
                   "last_noted_at",
                   "is_rating_locked",
                   "parent_id",
                   "has_children",
                   "approver_id",
                   "file_size",
                   "is_status_locked",
                   "up_score",
                   "down_score",
                   "is_pending",
                   "is_flagged",
                   "is_deleted",
                   "updated_at",
                   "is_banned",
                   "pixiv_id")

    # Create tables
    # In new database, id -> image_id
    c.execute('''CREATE TABLE images
                 (image_id INT PRIMARY KEY,
                  created_at TEXT,
                  uploaded_id INT,
                  score INT,
                  source TEXT,
                  md5 TEXT,
                  last_commented_at TEXT,
                  rating TEXT,
                  image_width INT,
                  image_height INT,
                  is_note_locked INT,
                  file_ext TEXT,
                  last_noted_at TEXT,
                  is_rating_locked INT,
                  parent_id INT,
                  has_children INT,
                  approver_id INT,
                  file_size INT,
                  is_status_locked INT,
                  up_score INT,
                  down_score INT,
                  is_pending INT,
                  is_flagged INT,
                  is_deleted INT,
                  updated_at TEXT,
                  is_banned INT,
                  pixiv_id INT,
                  hidden INT DEFAULT 0)''')

    # tags
    c.execute('''CREATE TABLE tags
                 (tag_id INT PRIMARY KEY,
                  name TEXT,
                  category INT)''')

    # tags <> images
    c.execute('''CREATE TABLE imageTags
                 (image_id INT,
                  tag_id INT,
                  PRIMARY KEY(image_id,tag_id))''')

    # KBR disable 'pools' handling. The interpretation of pools
    # data in the original script was incorrect. In the JSON, the pools data 
    # looks like (e.g.) "pools":["10152","4162","series","collection"],
    # which means (poolid=10152,type=series),(poolid=4162,type=collection)
    # # pools
    # c.execute('''CREATE TABLE pools
                 # (pool_id INT PRIMARY KEY,
                  # pool_type TEXT)''')
                  
    # # pools <> images
    # c.execute('''CREATE TABLE imagePools
                 # (image_id INT,
                  # pool_id INT,
                  # PRIMARY KEY(image_id,pool_id))''')

    # KBR Personal choice to not track the danbooru 'favorites' data
    # # list of values -> faver_id
    # c.execute('''CREATE TABLE favs
                 # (image_id INT,
                  # faver_id TEXT,
                  # PRIMARY KEY (image_id, faver_id))''')

    # KBR add useful indices when looking up images by tag    
    c.execute('CREATE INDEX tags_ids on tags(tag_id)')
    c.execute('CREATE INDEX tags_dex on tags(name,tag_id)')
    c.execute('CREATE INDEX image_ids on images(image_id)')
    c.execute('CREATE INDEX image_tags on imageTags(tag_id)')
    # useful index for looking up image by rating
    c.execute('CREATE INDEX image_rate on images(image_id,rating)')
    c.execute('CREATE INDEX image_hide on images(image_id,hidden)')
    
    
    for json_file in os.listdir(DATA_DIR):
        json_path = os.path.join(DATA_DIR, json_file)
        print("Processing", json_path)

        with open(json_path, encoding="UTF-8") as f:
            raw_json_lines = f.readlines()


        for raw_json_line in raw_json_lines:
            json_line = json.loads(raw_json_line)
            image_id = json_line["id"]

            # KBR Qwent's 2019 fileset stops at 3734659 - don't record metadata
            # beyond that value
            if (int)(image_id) > 3734659:
                continue;
                
            # table INSERTs
            images_values = list(json_line[key] for key in images_keys)
            images_values.append(0) # for 'hidden' column
            
            # a little messy
            c.execute("INSERT INTO images VALUES (" + ','.join('?'*28) + ")",
                      images_values)

            tags_values = ((tag["id"], tag["name"], tag["category"])
                           for tag in json_line["tags"])
            # duplicated tags: ex. image_id 931532, tag_id 535673
            c.executemany("INSERT OR IGNORE INTO tags VALUES (?,?,?)",
                          tags_values)

            imageTagValues = ((image_id, tag["id"])
                             for tag in json_line["tags"])
            c.executemany("INSERT OR IGNORE INTO imageTags VALUES (?,?)",
                          imageTagValues)
             
            # KBR disable pools handling [see above]
            # pools_values = ((image_id, pool) for pool in json_line["pools"])
            # c.executemany("INSERT OR IGNORE INTO pools VALUES (?,?)",
                          # pools_values)

            # KBR Personal choice to not track the danbooru 'favorites' data
            # favs_values = \
                # ((image_id, faver_id) for faver_id in json_line["favs"])
            # c.executemany("INSERT OR IGNORE INTO favs VALUES (?,?)",
                          # favs_values)
        
        conn.commit()

    #add a count of each tag to the tag table
    c.execute("alter table tags add count int default 0")
    c.execute("""update tags set count=
                 (select count(image_id) from imagetags where imagetags.tag_id=tags.tag_id) 
                  where exists 
                  (select * from imagetags where imagetags.tag_id = tags.tag_id)""")
    conn.commit()
    
    conn.close()

if __name__ == "__main__":
    main()


# select I.image_id,I.created_at,I.score,I.source,I.rating,I.image_width,I.image_height,I.file_size
# from images I
# join imageTags IT on I.image_id = IT.image_id
# join tags T on IT.tag_id = T.tag_id
# where T.name = 'touhou'
# order by I.image_id
