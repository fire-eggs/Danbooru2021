# When downloading the pools metadata directly from Danbooru,
# the post_count value is as of the download datetime.
#
# Correct the post_count value to be as of Gwern's download.
#
import sqlite3

conn = sqlite3.connect("danbooru2019.db")
c = conn.cursor()

c.execute("select pool_id from pools")
pool_ids = [i[0] for i in c.fetchall()]

for pid in pool_ids:
    c.execute("select count(image_id) from imagePools where pool_id=?",(pid,))
    count = c.fetchall()[0][0]
    c.execute("update pools set post_count=? where pool_id=?",(count,pid))
    conn.commit()
conn.close()

