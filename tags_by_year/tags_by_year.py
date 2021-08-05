# Fetch copyright tags by image, accumulating them by the year the image was posted.
# Generates a csv file which can be imported into "excel".
# Years range from 2005 to 2021
# The CSV is written to stdout, pipe it to your output file.

import os
import sys
import sqlite3

conn = sqlite3.connect("db2020.db")
conn.isolation_level = None
cur = conn.cursor()

tags = {}  # dictionary where the key is the tag name; the value is a dictionary of year

# Fetch image-id, year and month posted, and all copyright tags for said image.
# tag.category=3 is "copyright"
# tag_id of 18 is "original", i.e. no copyright/subject
cur.execute(
'''select I.image_id, substr(I.created_at,1,4) as Year, substr(I.created_at,6,2) as Mon, T.tag_id, T.name from images I join imageTags IT on I.image_id=IT.image_id join tags T on IT.tag_id = T.tag_id 
where T.category=3 AND T.tag_id != 18 order by T.tag_id'''
)

while True:
  res = cur.fetchmany(10000)
  
  if not res:
    break
    
  for row in res:
    tag = row[4]     # tag name
    bucket = row[1]  # year
    if tag in tags:
      # tag already in dictionary. accumulate this row into a year bucket
      bucketdict = tags[tag]
      if bucket in bucketdict:
        bucketdict[bucket] = bucketdict[bucket] + 1
      else:
        bucketdict[bucket] = 1
    else:
      # new tag for the dictionary, create and initialize the year dictionary
      bucketdict = {}
      bucketdict[bucket] = 1
      tags[tag] = bucketdict
    
conn.close()

# alphabetic in order of tag-name
for first in sorted(tags):
  outl = ["'" + first+"'"]   # tag name with single-quote delimiters
  outl.append(0)             # placeholder for total
  
  buckets = tags[first]      # year buckets for this tag
  
  # insure all buckets exist
  for i in range(2005,2021):
    if str(i) not in buckets:
      buckets[str(i)] = 0
  
  total = 0 # accumulate total
  for bucket in sorted(tags[first]):
    total = total + tags[first][bucket]
    outl.append(str(tags[first][bucket])) # append each bucket to the list
    
  outl[1] = str(total)  # store total
  
  csvl = ";".join(outl)  # semi-colon separated
  print(csvl)
