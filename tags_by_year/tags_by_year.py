
import os
import sys
import sqlite3

conn = sqlite3.connect("db2020.db")
conn.isolation_level = None
cur = conn.cursor()


tags = {}

cur.execute(
'''select I.image_id, substr(I.created_at,1,4) as Year, substr(I.created_at,6,2) as Mon, T.tag_id, T.name from images I join imageTags IT on I.image_id=IT.image_id join tags T on IT.tag_id = T.tag_id 
where T.category=3 AND T.tag_id != 18 order by T.tag_id'''
)
loopcount = 1
while True:
  res = cur.fetchmany(10000)
  
  if not res:
    break
    
  for row in res:
    # group tags by year, month
    #print(res[0][4], int(res[0][1]), int(res[0][2]))
    tag = row[4]
    #bucket = row[1]+row[2] # year+month
    bucket = row[1]         # year
    if tag in tags:
      bucketdict = tags[tag]
      if bucket in bucketdict:
        bucketdict[bucket] = bucketdict[bucket] + 1
      else:
        bucketdict[bucket] = 1
    else:
      bucketdict = {}
      bucketdict[bucket] = 1
      tags[tag] = bucketdict
    
#  loopcount = loopcount + 1
#  if loopcount > 100:
#    break

conn.close()
    
for first in sorted(tags):
#first = list(tags)[0]
  outl = ["'" + first+"'"]
  outl.append(0)
  
  #print(first)
  buckets = tags[first]
  
  # insure all buckets exist
  for i in range(2005,2021):
    if str(i) not in buckets:
      buckets[str(i)] = 0
  
  total = 0
  for bucket in sorted(tags[first]):
    total = total + tags[first][bucket]
    outl.append(str(tags[first][bucket]))
    #print(bucket + ":" + str(tags[first][bucket]))
  outl[1] = str(total)
  
  csvl = ";".join(outl)
  print(csvl)
