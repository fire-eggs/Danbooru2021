# Script to import the pools data from Gwern's JSON metadata.
# This assumes the database has been built _without_ the pools
# data; this is an update.
#
# Gwern's metadata only contains the pool ids and the image ids
# belonging to those pools. The next step after this is to d/l
# the pool metadata from Danbooru using their API.
#
import sqlite3
import json
import os

# json files are in the following folder
DATA_DIR = "metadata"

conn = sqlite3.connect("danbooru2019.db")
c = conn.cursor()

c.execute("select count(name) from sqlite_master where type='table' and name='pools'")
if c.fetchone()[0] != 0:
    print("Pools table already exists. Bailing.")
    exit()

# Create the table/columns to hold the pool metadata we care about.
# The 'user_pool' field is intended to implement the "favorites" feature.
c.execute('''create table pools
          (pool_id INT PRIMARY KEY,
           name TEXT,
           desc TEXT,
           is_active INT,
           is_deleted INT,
           post_count INT,
           date TEXT,
           user_pool INT)
           ''')
c.execute('''CREATE TABLE imagePools
             (image_id INT,
              pool_id INT,
              PRIMARY KEY(image_id,pool_id))''')
              
c.execute('CREATE INDEX image_pools on imagePools(pool_id)')
c.execute('CREATE INDEX pools_dex on pools(name,pool_id)')
              
for json_file in os.listdir(DATA_DIR):
    json_path = os.path.join(DATA_DIR, json_file)
    print("Processing", json_path)

    with open(json_path, encoding="UTF-8") as f:
        raw_json_lines = f.readlines()


    for raw_json_line in raw_json_lines:
        json_line = json.loads(raw_json_line)
        image_id = json_line["id"]

        # KBR Gwern's 2019 fileset stops at 3734659 - don't record metadata
        # beyond that value
        if (int)(image_id) > 3734659:
            continue;

        pools_values = [pool for pool in json_line["pools"]]
        # In the JSON, the pools values look like (e.g.):
        # "pools":["10152","4162","series","collection"]
        # which means only the first half of the pools values are useful
        half = (int)(len(pools_values) / 2)
        for pool in pools_values[:half]:
            c.execute("INSERT OR IGNORE INTO pools values (?,'','',0,0,0,'',0)", (pool,))
            c.execute("INSERT OR IGNORE INTO imagePools values (?,?)", (image_id,pool))

    conn.commit()
    
conn.close()
