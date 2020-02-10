# Fetch pool metadata from Danbooru using their API.
#
# Gwern's metadata only indicates which pools the images belong to,
# not any metadata about the pools.
#
import requests
import json
import sqlite3
import time

# the JSON entries we'll store
pool_keys=("name","description","is_active","is_deleted","post_count","updated_at")

# danbooru api base URL
base = "https://danbooru.donmai.us/pools.json?search[id]="

conn = sqlite3.connect("danbooru2019.db")
c = conn.cursor()

# all unprocessed pools. Assumes nothing has been processed
last = 0
c.execute("select pool_id from pools where pool_id > ?",(last,))
pool_ids = [i[0] for i in c.fetchall()]

# split pool_ids into slices of 10

for i in range(0, len(pool_ids), 10):
    ids = pool_ids[i:i+10]
    id_str = ",".join([str(x) for x in ids])
    print(id_str)
    
    url = base + id_str
    response = requests.get(url)
    if response.status_code != 200:
        print("Fail " + str(id))
    else:
        respj = response.json()
    
        for aval in respj:
            thisid = aval["id"]
            pools_values = list(aval[key] for key in pool_keys)
            pools_values.append(thisid)
            c.execute("""update or ignore pools set 
                         (name,desc,is_active,is_deleted,
                          post_count,date)=("""+
                          ",".join('?'*len(pool_keys))+") where pool_id=?",pools_values)
    conn.commit()
    time.sleep(10)
conn.close()
